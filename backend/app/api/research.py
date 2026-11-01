from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status, UploadFile, File, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import func
from typing import List
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
from io import BytesIO
from pathlib import Path
from uuid import UUID

from app.core.database import get_db, AsyncSessionLocal
from app.core.config import settings
from app.models.database import ResearchSession, Source
from app.core.security import user_id_from_request
from app.schemas.research import (
    ResearchSessionCreate, ResearchSessionResponse, ResearchScopeResponse,
    ResearchGoal, ResearchDimension, DimensionUpdate, SourceCreate, SourceResponse,
    GapResponse,
    SessionStatusResponse, SessionStatus, ResearchResultsResponse,
    ChecklistUpdate, VerificationTaskResponse, ConflictResponse, ClaimResponse,
)
from app.pipeline.orchestrator import run_pipeline
from app.services.topic_guardrails import TopicGuardError, validate_research_goal

async def require_user_session_access(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = user_id_from_request(request)
    request.state.user_id = user_id
    session_id = request.path_params.get("session_id")
    if session_id:
        result = await db.execute(select(ResearchSession.id).where(
            ResearchSession.id == session_id,
            ResearchSession.owner_id == user_id,
        ))
        if result.scalar_one_or_none() is None:
            # Deliberately return the same result for missing and another user's session.
            raise HTTPException(status_code=404, detail="Research session not found.")


router = APIRouter(prefix="/api/research", tags=["research"], dependencies=[Depends(require_user_session_access)])


@router.get("", response_model=List[ResearchSessionResponse])
async def list_research_sessions(request: Request, db: AsyncSession = Depends(get_db)):
    """List recent persisted sessions for the home screen."""
    result = await db.execute(
        select(ResearchSession).where(ResearchSession.owner_id == request.state.user_id).order_by(ResearchSession.updated_at.desc()).limit(50)
    )
    sessions = result.scalars().all()
    counts_result = await db.execute(
        select(Source.session_id, func.count(Source.id))
        .where(Source.session_id.in_([s.id for s in sessions]))
        .group_by(Source.session_id)
    ) if sessions else None
    source_counts = dict(counts_result.all()) if counts_result else {}
    return [ResearchSessionResponse(
        id=str(item.id), goal=item.goal_text, status=item.status,
        created_at=item.created_at, updated_at=item.updated_at,
        source_count=source_counts.get(item.id, 0),
        dimension_count=len(item.dimensions_json or []),
        is_partial=item.is_partial or False, error=item.error,
    ) for item in sessions]


@router.post("", response_model=ResearchSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_research(
    request: Request,
    payload: ResearchSessionCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new research session."""
    try:
        await validate_research_goal(payload.goal)
    except TopicGuardError as exc:
        detail = {"code": exc.code, "message": str(exc)} if exc.code.startswith("guardrail_") else str(exc)
        raise HTTPException(status_code=exc.status_code, detail=detail) from exc

    unsupported_files = [source for source in payload.sources if source.kind == "file"]
    if unsupported_files:
        raise HTTPException(status_code=422, detail="Upload documents after creating the research session.")
    source_urls = list(dict.fromkeys(str(source.url) for source in payload.sources if source.url))
    if len(source_urls) > settings.MAX_SOURCES_PER_SESSION:
        raise HTTPException(status_code=422, detail=f"At most {settings.MAX_SOURCES_PER_SESSION} source URLs are allowed.")
    if payload.user_dimensions and len(payload.user_dimensions) > settings.MAX_DIMENSIONS:
        raise HTTPException(status_code=422, detail=f"At most {settings.MAX_DIMENSIONS} initial dimensions are allowed.")

    session = ResearchSession(
        goal_text=payload.goal,
        goal_json={
            "original_query": payload.goal,
            "interpreted_objective": "",
            "entities": [],
            "scope": [],
            "geography": [],
            "time_constraints": None,
            "constraints": [],
        },
        dimensions_json=[dimension.model_dump(mode="json") for dimension in (payload.user_dimensions or [])],
        status=SessionStatus.CREATED,
        owner_id=request.state.user_id,
    )
    db.add(session)
    # Persist URL inputs with the session so they are extracted alongside search results.
    from app.models.database import Source
    from urllib.parse import urlparse
    for url in source_urls:
        session.sources.append(Source(
            url=url,
            domain=urlparse(url).netloc,
            extraction_status="pending",
        ))
    await db.commit()
    await db.refresh(session)
    
    return ResearchSessionResponse(
        id=session.id,
        goal=session.goal_text,
        status=session.status,
        created_at=session.created_at,
        updated_at=session.updated_at,
        source_count=len(source_urls),
        dimension_count=0,
    )


@router.post("/{session_id}/sources/upload", response_model=List[SourceResponse], status_code=status.HTTP_201_CREATED)
async def upload_sources(
    session_id: str,
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Extract text from supported documents and persist them as research sources."""
    try:
        session_uuid = UUID(session_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid session ID.") from exc
    result = await db.execute(select(ResearchSession).where(ResearchSession.id == str(session_uuid)))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session.status not in (SessionStatus.CREATED, SessionStatus.SCOPE_REVIEW):
        raise HTTPException(status_code=409, detail="Documents can only be added before research starts.")
    if not files:
        raise HTTPException(status_code=422, detail="Select at least one document.")

    from app.models.database import Source
    existing_result = await db.execute(select(Source).where(Source.session_id == str(session_uuid)))
    existing_sources = existing_result.scalars().all()
    if len(existing_sources) + len(files) > settings.MAX_SOURCES_PER_SESSION:
        raise HTTPException(status_code=422, detail=f"At most {settings.MAX_SOURCES_PER_SESSION} sources are allowed per session.")

    created = []
    for upload in files:
        name = Path((upload.filename or "document").replace("\\", "/")).name
        ext = Path(name).suffix.lower()
        if ext not in {".pdf", ".docx", ".txt"}:
            raise HTTPException(status_code=415, detail=f"{name}: supported formats are PDF, DOCX, and TXT.")
        data = await upload.read(10 * 1024 * 1024 + 1)
        if len(data) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail=f"{name}: maximum file size is 10 MB.")
        try:
            if ext == ".txt":
                content = data.decode("utf-8-sig").strip()
            elif ext == ".pdf":
                try:
                    from pypdf import PdfReader
                    content = "\n".join((page.extract_text() or "") for page in PdfReader(BytesIO(data)).pages).strip()
                except ImportError:
                    import fitz
                    document = fitz.open(stream=data, filetype="pdf")
                    content = "\n".join(page.get_text() for page in document).strip()
            else:
                from docx import Document
                document = Document(BytesIO(data))
                paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
                for table in document.tables:
                    paragraphs.extend(" | ".join(cell.text.strip() for cell in row.cells) for row in table.rows)
                content = "\n".join(paragraphs).strip()
        except Exception as exc:
            raise HTTPException(status_code=422, detail=f"{name}: could not read this document ({exc}).") from exc
        if not content:
            raise HTTPException(status_code=422, detail=f"{name}: no extractable text found. Scanned PDFs need OCR and are not supported.")
        source = Source(
            session_id=str(session_uuid), url=None, title=name, domain="Uploaded document",
            extraction_status="success", content=content,
            metadata_json={"kind": "upload", "filename": name, "content_type": upload.content_type, "bytes": len(data)},
        )
        db.add(source)
        created.append(source)
    await db.commit()
    for source in created:
        await db.refresh(source)
    return [SourceResponse(
        id=str(source.id), session_id=str(source.session_id), url=source.url,
        title=source.title, domain=source.domain, source_type=source.source_type,
        publication_date=source.publication_date, last_modified=source.last_modified,
        retrieval_date=source.retrieval_date, authority_score=source.authority_score,
        relevance_score=source.relevance_score, extraction_status=source.extraction_status,
        content_preview=source.content[:500],
    ) for source in created]


@router.post("/{session_id}/understand", response_model=ResearchScopeResponse)
async def understand_goal(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Generate goal understanding and research dimensions (Stage 1-2)."""
    result = await db.execute(
        select(ResearchSession).where(ResearchSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.status == SessionStatus.SCOPE_REVIEW and session.dimensions_json:
        return ResearchScopeResponse(
            session_id=session_id,
            goal_understanding=ResearchGoal(**session.goal_json),
            dimensions=[ResearchDimension(**d) for d in session.dimensions_json],
            status=session.status,
        )
    retryable_scope_failure = (
        session.status == SessionStatus.FAILED
        and not session.dimensions_json
        and (session.error or "").startswith("Scope generation failed:")
    )
    if session.status != SessionStatus.CREATED and not retryable_scope_failure:
        raise HTTPException(status_code=409, detail=f"Cannot generate scope while session is {session.status.value}.")

    # Claim the understanding stage atomically so a refresh or duplicate request
    # cannot run two LLM generations against the same session at once.
    from sqlalchemy import update
    from datetime import datetime
    claimed = await db.execute(
        update(ResearchSession)
        .where(
            ResearchSession.id == session_id,
            ResearchSession.status == session.status,
        )
        .values(status=SessionStatus.UNDERSTANDING, updated_at=datetime.utcnow())
    )
    if claimed.rowcount != 1:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Research scope generation is already running. Reload this session shortly.")
    await db.commit()

    # Import here to avoid circular imports
    from app.pipeline.orchestrator import PipelineOrchestrator
    
    orchestrator = PipelineOrchestrator(db)
    orchestrator.session_id = session_id
    
    # Run understanding and dimension generation
    try:
        await orchestrator._emit_progress("understanding", None, "Interpreting this session's research goal")
        goal = await orchestrator._stage_understand_goal()
        await orchestrator._emit_progress("dimensions", None, "Generating dimensions from this session's goal")
        dimensions = await orchestrator._stage_generate_dimensions(goal)
        await db.execute(
            update(ResearchSession)
            .where(ResearchSession.id == session_id, ResearchSession.status == SessionStatus.UNDERSTANDING)
            .values(status=SessionStatus.SCOPE_REVIEW, error=None, updated_at=datetime.utcnow())
        )
        await db.commit()
        await orchestrator._emit_progress("scope_review", None, "Research dimensions are ready for your review")
    except Exception as exc:
        await db.rollback()
        await db.execute(
            update(ResearchSession)
            .where(ResearchSession.id == session_id, ResearchSession.status == SessionStatus.UNDERSTANDING)
            .values(status=SessionStatus.FAILED, error=f"Scope generation failed: {exc}", updated_at=datetime.utcnow())
        )
        await db.commit()
        raise HTTPException(status_code=502, detail=f"Could not generate research scope: {exc}") from exc
    
    return ResearchScopeResponse(
        session_id=session_id,
        goal_understanding=goal,
        dimensions=dimensions,
        status=SessionStatus.SCOPE_REVIEW,
    )


@router.get("/{session_id}/scope", response_model=ResearchScopeResponse)
async def get_scope(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get current research scope (dimensions)."""
    result = await db.execute(
        select(ResearchSession).where(ResearchSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    dimensions = [
        ResearchDimension(**d) for d in session.dimensions_json
    ]
    goal = ResearchGoal(**session.goal_json)
    
    return ResearchScopeResponse(
        session_id=session_id,
        goal_understanding=goal,
        dimensions=dimensions,
        status=session.status,
    )


@router.patch("/{session_id}/scope", response_model=ResearchScopeResponse)
async def update_scope(
    session_id: str,
    payload: DimensionUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update research dimensions."""
    from sqlalchemy import update
    from datetime import datetime
    
    result = await db.execute(
        select(ResearchSession).where(ResearchSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != SessionStatus.SCOPE_REVIEW:
        raise HTTPException(status_code=409, detail=f"Scope can only be edited during scope_review; current state is {session.status.value}.")
    if not payload.dimensions:
        raise HTTPException(status_code=422, detail="At least one research dimension is required.")
    if len(payload.dimensions) > settings.MAX_DIMENSIONS:
        raise HTTPException(status_code=422, detail=f"At most {settings.MAX_DIMENSIONS} dimensions are allowed.")
    
    dims_json = [d.model_dump() for d in payload.dimensions]
    
    result = await db.execute(
        update(ResearchSession)
        .where(ResearchSession.id == session_id, ResearchSession.status == SessionStatus.SCOPE_REVIEW)
        .values(dimensions_json=dims_json, updated_at=datetime.utcnow())
    )
    if result.rowcount != 1:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Research started while the scope was being saved. Reload the session.")
    await db.commit()
    
    goal = ResearchGoal(**session.goal_json)
    dimensions = [ResearchDimension(**d) for d in dims_json]
    
    return ResearchScopeResponse(
        session_id=session_id,
        goal_understanding=goal,
        dimensions=dimensions,
        status=session.status,
    )


@router.post("/{session_id}/start")
async def start_research(
    session_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Start the research pipeline (transition from SCOPE_REVIEW to pipeline)."""
    from sqlalchemy import update
    from datetime import datetime
    
    result = await db.execute(
        select(ResearchSession).where(ResearchSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.status != SessionStatus.SCOPE_REVIEW:
        raise HTTPException(status_code=409, detail=f"Session cannot start from state {session.status.value}.")
    if not session.dimensions_json:
        raise HTTPException(status_code=422, detail="Save at least one research dimension before starting.")
    
    # Update status to READY (pipeline will pick up)
    result = await db.execute(
        update(ResearchSession)
        .where(ResearchSession.id == session_id, ResearchSession.status == SessionStatus.SCOPE_REVIEW)
        .values(status=SessionStatus.READY, updated_at=datetime.utcnow())
    )
    if result.rowcount != 1:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Research was started by another request.")
    await db.commit()
    
    # Start pipeline in background
    from app.pipeline.orchestrator import ACTIVE_PIPELINE_PROGRESS
    ACTIVE_PIPELINE_PROGRESS.pop(session_id, None)
    background_tasks.add_task(run_pipeline, session_id)
    
    return {"message": "Research started", "session_id": session_id}


@router.post("/{session_id}/resume-checklist")
async def resume_saved_checklist(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Finish a run whose durable research analysis stopped while persisting checklist rows."""
    from datetime import datetime
    from sqlalchemy import update
    from app.models.database import Claim, Gap, ChecklistItem
    from app.pipeline.orchestrator import PipelineOrchestrator

    result = await db.execute(select(ResearchSession).where(ResearchSession.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session.status != SessionStatus.FAILED or not session.error or "class 'builtins.list' is not mapped" not in session.error.lower():
        raise HTTPException(status_code=409, detail="This session did not stop at the recoverable checklist-save error.")

    sources_result = await db.execute(select(Source).where(Source.session_id == session_id))
    sources = sources_result.scalars().all()
    challenge_markers = ("checking your browser", "recaptcha", "captcha challenge", "verify you are human", "access denied", "cloudflare ray id")
    for source in sources:
        opening = f"{source.title or ''}\n{(source.content or '')[:600]}".casefold()
        if any(marker in opening for marker in challenge_markers):
            source.extraction_status = "failed"
    gaps_result = await db.execute(select(Gap).where(Gap.session_id == session_id))
    gaps = gaps_result.scalars().all()
    if not sources or not gaps:
        raise HTTPException(status_code=409, detail="The session has no saved source and gap results to finish.")
    claims_result = await db.execute(select(Claim).where(Claim.session_id == session_id))
    claims = claims_result.scalars().all()
    checklist_result = await db.execute(select(ChecklistItem).where(ChecklistItem.session_id == session_id))
    existing_tasks = checklist_result.scalars().all()
    existing_dimensions = {task.dimension_id for task in existing_tasks}
    missing_gaps = [gap for gap in gaps if gap.dimension_id not in existing_dimensions]
    if missing_gaps:
        orchestrator = PipelineOrchestrator(db)
        orchestrator.session_id = session_id
        await orchestrator._stage_verification_checklist(missing_gaps, claims, sources)

    claimed_source_ids = {claim.source_id for claim in claims}
    partial = any(source.extraction_status != "success" for source in sources) or any(source.id not in claimed_source_ids for source in sources)
    recovery_note = "Some sources did not produce extracted claims; review the partial results." if partial else None
    await db.execute(
        update(ResearchSession)
        .where(ResearchSession.id == session_id, ResearchSession.status == SessionStatus.FAILED)
        .values(
            status=SessionStatus.PARTIAL if partial else SessionStatus.COMPLETED,
            is_partial=partial,
            error=recovery_note,
            completed_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
    )
    await db.commit()
    return {
        "session_id": session_id,
        "status": SessionStatus.PARTIAL.value if partial else SessionStatus.COMPLETED.value,
        "is_partial": partial,
        "checklist_tasks": len(existing_tasks) + len(missing_gaps),
        "message": "Saved results were recovered. No search or model requests were repeated.",
    }


@router.get("/{session_id}/events")
async def sse_events(
    session_id: str,
):
    """SSE endpoint for real-time progress updates."""
    async with AsyncSessionLocal() as db:
        exists = await db.scalar(select(ResearchSession.id).where(ResearchSession.id == session_id))
        if not exists:
            raise HTTPException(status_code=404, detail="Session not found")
    
    async def event_generator():
        last_update = None
        while True:
            async with AsyncSessionLocal() as stream_db:
                result = await stream_db.execute(
                    select(ResearchSession).where(ResearchSession.id == session_id)
                )
                session = result.scalar_one_or_none()
                if not session:
                    yield {"event": "error", "data": json.dumps({"error": "Session not found"})}
                    break
                current_update = session.updated_at
                state = session.status.value
                updated_at = session.updated_at.isoformat() if session.updated_at else None
                partial = session.is_partial
                current_error = session.error
            if current_update != last_update:
                last_update = current_update
                
                data = {
                    "session_id": session_id,
                    "status": state,
                    "updated_at": updated_at,
                    "is_partial": partial,
                    "error": current_error,
                }
                yield {"event": "progress", "data": json.dumps(data)}
            
            # Check for completion
            if state in [SessionStatus.COMPLETED.value, SessionStatus.FAILED.value, SessionStatus.PARTIAL.value]:
                yield {"event": "complete", "data": json.dumps({"status": state, "is_partial": partial, "error": current_error})}
                break
            
            await asyncio.sleep(1)
    
    return EventSourceResponse(event_generator(), ping=15)


@router.get("/{session_id}/status", response_model=SessionStatusResponse)
async def get_status(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get current pipeline status."""
    result = await db.execute(
        select(ResearchSession).where(ResearchSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Count sources and claims
    from app.models.database import Source, Claim
    from sqlalchemy import func
    
    source_count = await db.scalar(
        select(func.count(Source.id)).where(Source.session_id == session_id)
    )
    claim_count = await db.scalar(
        select(func.count(Claim.id)).where(Claim.session_id == session_id)
    )
    from app.models.database import Gap
    gap_count = await db.scalar(select(func.count(Gap.id)).where(Gap.session_id == session_id))
    can_resume = (
        session.status == SessionStatus.FAILED
        and bool(source_count)
        and bool(gap_count)
        and session.error is not None
        and "class 'builtins.list' is not mapped" in session.error.lower()
    )
    
    stages = [
        "understanding", "dimensions", "scope_review", "query_planning",
        "searching", "extracting", "chunking", "claims",
        "coverage", "contradictions", "freshness", "evidence",
        "gaps", "checklist",
    ]
    
    stage_state = {
        SessionStatus.CREATED: (0, "understanding", 0),
        SessionStatus.UNDERSTANDING: (5, "understanding", 0),
        SessionStatus.SCOPE_REVIEW: (15, "scope_review", 3),
        SessionStatus.READY: (20, "query_planning", 3),
        SessionStatus.SEARCHING: (30, "searching", 4),
        SessionStatus.EXTRACTING: (45, "extracting", 5),
        SessionStatus.CLAIM_EXTRACTION: (60, "claims", 7),
        SessionStatus.ANALYZING: (70, "coverage and evidence analysis", 8),
        SessionStatus.GENERATING_CHECKLIST: (90, "checklist", 13),
        SessionStatus.COMPLETED: (100, "completed", len(stages)),
        SessionStatus.PARTIAL: (100, "completed with partial results", len(stages)),
        SessionStatus.FAILED: (0, "failed", 0),
    }
    progress, current_stage, completed_idx = stage_state[session.status]
    from app.pipeline.orchestrator import ACTIVE_PIPELINE_PROGRESS
    live = ACTIVE_PIPELINE_PROGRESS.get(session_id)
    if live and session.status not in (SessionStatus.COMPLETED, SessionStatus.PARTIAL):
        current_stage = live["current_stage"]
        completed_stages = live["stages_completed"]
        pending_stages = live["stages_pending"]
        current_message = session.error if session.status == SessionStatus.FAILED else live.get("current_message")
    else:
        completed_stages = stages[:completed_idx]
        pending_stages = stages[completed_idx:]
        current_message = None
    if session.status in (SessionStatus.COMPLETED, SessionStatus.PARTIAL):
        completed_stages, pending_stages = stages, []
    if session.status == SessionStatus.FAILED and can_resume and not live:
        checklist_index = stages.index("checklist")
        current_stage = "checklist"
        current_message = session.error
        completed_stages = stages[:checklist_index]
        pending_stages = []
    elif session.status == SessionStatus.FAILED and not live:
        current_stage = "failed"
    
    return SessionStatusResponse(
        session_id=session_id,
        status=session.status,
        current_stage=current_stage,
        current_message=current_message,
        progress=progress,
        stages_completed=completed_stages,
        stages_pending=pending_stages,
        sources_found=source_count or 0,
        claims_extracted=claim_count or 0,
        errors=[session.error] if session.error else [],
        is_partial=session.is_partial,
        can_resume=can_resume,
    )


@router.get("/{session_id}/results", response_model=ResearchResultsResponse)
async def get_results(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get complete research results."""
    from app.models.database import Source, Claim, Gap, Conflict, ChecklistItem
    from app.schemas.research import (
        SourceResponse, ClaimResponse, GapResponse, ConflictResponse,
        VerificationTaskResponse, ResearchGoal, ResearchDimension,
    )
    from sqlalchemy import select
    
    result = await db.execute(
        select(ResearchSession).where(ResearchSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Load related data
    sources_result = await db.execute(
        select(Source).where(Source.session_id == session_id)
    )
    sources = sources_result.scalars().all()
    
    claims_result = await db.execute(
        select(Claim).where(Claim.session_id == session_id)
    )
    claims = claims_result.scalars().all()
    
    gaps_result = await db.execute(
        select(Gap).where(Gap.session_id == session_id)
    )
    gaps = gaps_result.scalars().all()
    
    from sqlalchemy.orm import selectinload
    conflicts_result = await db.execute(
        select(Conflict).options(selectinload(Conflict.claim_a), selectinload(Conflict.claim_b)).where(Conflict.session_id == session_id)
    )
    conflicts = conflicts_result.scalars().all()
    
    checklist_result = await db.execute(
        select(ChecklistItem).where(ChecklistItem.session_id == session_id)
    )
    checklist = checklist_result.scalars().all()
    
    # Convert to response models
    source_responses = [
        SourceResponse(
            id=s.id,
            session_id=s.session_id,
            url=s.url,
            title=s.title,
            domain=s.domain,
            source_type=s.source_type,
            publication_date=s.publication_date,
            last_modified=s.last_modified,
            retrieval_date=s.retrieval_date,
            authority_score=s.authority_score,
            relevance_score=s.relevance_score,
            extraction_status=s.extraction_status,
            content_preview=s.content[:200] if s.content else None,
        )
        for s in sources
    ]
    
    claim_responses = [
        ClaimResponse(
            id=c.id,
            session_id=c.session_id,
            source_id=c.source_id,
            dimension_id=c.dimension_id,
            text=c.claim_text,
            entity=c.entity,
            attribute=c.attribute,
            value=c.value,
            claim_type=c.claim_type,
            excerpt=c.excerpt,
            confidence=c.confidence,
            evidence_status=c.evidence_status,
            freshness=c.freshness,
        )
        for c in claims
    ]
    
    gap_responses = [
        GapResponse(
            id=g.id,
            session_id=g.session_id,
            dimension_id=g.dimension_id,
            title=g.title,
            explanation=g.explanation,
            priority=g.priority,
            evidence_summary=g.evidence_summary,
            next_action=g.next_action,
            recommended_authority=g.recommended_authority,
            verification_method=g.verification_method,
            source_ids=g.source_ids or [],
        )
        for g in gaps
    ]
    
    conflict_responses = [
        ConflictResponse(
            id=c.id,
            session_id=c.session_id,
            entity=c.entity,
            attribute=c.attribute,
            claim_a=ClaimResponse(
                id=c.claim_a.id,
                session_id=c.claim_a.session_id,
                source_id=c.claim_a.source_id,
                dimension_id=c.claim_a.dimension_id,
                text=c.claim_a.claim_text,
                entity=c.claim_a.entity,
                attribute=c.claim_a.attribute,
                value=c.claim_a.value,
                claim_type=c.claim_a.claim_type,
                excerpt=c.claim_a.excerpt,
                confidence=c.claim_a.confidence,
                evidence_status=c.claim_a.evidence_status,
            ),
            claim_b=ClaimResponse(
                id=c.claim_b.id,
                session_id=c.claim_b.session_id,
                source_id=c.claim_b.source_id,
                dimension_id=c.claim_b.dimension_id,
                text=c.claim_b.claim_text,
                entity=c.claim_b.entity,
                attribute=c.claim_b.attribute,
                value=c.claim_b.value,
                claim_type=c.claim_b.claim_type,
                excerpt=c.claim_b.excerpt,
                confidence=c.claim_b.confidence,
                evidence_status=c.claim_b.evidence_status,
            ),
            conflict_type=c.conflict_type,
            resolution_action=c.resolution_action,
        )
        for c in conflicts
    ]
    
    checklist_responses = [
        VerificationTaskResponse(
            id=c.id,
            session_id=c.session_id,
            dimension_id=c.dimension_id,
            title=c.title,
            priority=c.priority,
            explanation=c.explanation,
            completed=c.completed,
            recommended_authority=c.recommended_authority,
            verification_method=c.verification_method,
            source_ids=c.source_ids or [],
        )
        for c in checklist
    ]
    
    return ResearchResultsResponse(
        session_id=session_id,
        goal=ResearchGoal(**session.goal_json),
        dimensions=[ResearchDimension(**d) for d in session.dimensions_json],
        sources=source_responses,
        claims=claim_responses,
        gaps=gap_responses,
        conflicts=conflict_responses,
        checklist=checklist_responses,
        status=session.status,
        completed_at=session.completed_at,
        is_partial=session.is_partial,
    )


@router.get("/{session_id}/sources", response_model=List[SourceResponse])
async def get_sources(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get all sources for a session."""
    from app.models.database import Source
    from app.schemas.research import SourceResponse
    from sqlalchemy import select
    
    result = await db.execute(
        select(Source).where(Source.session_id == session_id)
    )
    sources = result.scalars().all()
    
    return [
        SourceResponse(
            id=s.id,
            session_id=s.session_id,
            url=s.url,
            title=s.title,
            domain=s.domain,
            source_type=s.source_type,
            publication_date=s.publication_date,
            last_modified=s.last_modified,
            retrieval_date=s.retrieval_date,
            authority_score=s.authority_score,
            relevance_score=s.relevance_score,
            extraction_status=s.extraction_status,
            content_preview=s.content[:200] if s.content else None,
        )
        for s in sources
    ]


@router.get("/{session_id}/sources/{source_id}/content")
async def get_source_content(
    session_id: str,
    source_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Return the extracted source text for evidence review within its session."""
    result = await db.execute(select(Source).where(
        Source.id == source_id,
        Source.session_id == session_id,
    ))
    source = result.scalar_one_or_none()
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found in this research session.")
    return {
        "id": str(source.id),
        "session_id": str(source.session_id),
        "title": source.title,
        "url": source.url,
        "extraction_status": source.extraction_status,
        "content": source.content or "",
    }


@router.get("/{session_id}/claims", response_model=List[ClaimResponse])
async def get_claims(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get all claims for a session."""
    from app.models.database import Claim
    from sqlalchemy import select
    
    result = await db.execute(
        select(Claim).where(Claim.session_id == session_id)
    )
    claims = result.scalars().all()
    
    return [
        {
            "id": c.id,
            "session_id": c.session_id,
            "source_id": c.source_id,
            "dimension_id": c.dimension_id,
            "text": c.claim_text,
            "entity": c.entity,
            "attribute": c.attribute,
            "value": c.value,
            "claim_type": c.claim_type,
            "excerpt": c.excerpt,
            "confidence": c.confidence,
            "evidence_status": c.evidence_status.value,
            "freshness": c.freshness,
        }
        for c in claims
    ]


@router.get("/{session_id}/gaps", response_model=List[GapResponse])
async def get_gaps(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get all gaps for a session."""
    from app.models.database import Gap
    from sqlalchemy import select
    
    result = await db.execute(
        select(Gap).where(Gap.session_id == session_id)
    )
    gaps = result.scalars().all()
    
    return [
        {
            "id": g.id,
            "session_id": g.session_id,
            "dimension_id": g.dimension_id,
            "title": g.title,
            "explanation": g.explanation,
            "priority": g.priority.value,
            "evidence_summary": g.evidence_summary,
            "next_action": g.next_action,
            "recommended_authority": g.recommended_authority,
            "verification_method": g.verification_method,
            "source_ids": g.source_ids or [],
        }
        for g in gaps
    ]


@router.get("/{session_id}/conflicts", response_model=List[ConflictResponse])
async def get_conflicts(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get all conflicts for a session."""
    from app.models.database import Conflict
    from app.schemas.research import ClaimResponse, ConflictResponse
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    result = await db.execute(
        select(Conflict).options(selectinload(Conflict.claim_a), selectinload(Conflict.claim_b)).where(Conflict.session_id == session_id)
    )
    conflicts = result.scalars().all()
    
    return [
        ConflictResponse(
            id=c.id,
            session_id=c.session_id,
            entity=c.entity,
            attribute=c.attribute,
            claim_a=ClaimResponse(id=c.claim_a.id, session_id=c.claim_a.session_id, source_id=c.claim_a.source_id, dimension_id=c.claim_a.dimension_id, text=c.claim_a.claim_text, entity=c.claim_a.entity, attribute=c.claim_a.attribute, value=c.claim_a.value, claim_type=c.claim_a.claim_type, excerpt=c.claim_a.excerpt, confidence=c.claim_a.confidence, evidence_status=c.claim_a.evidence_status, freshness=c.claim_a.freshness),
            claim_b=ClaimResponse(id=c.claim_b.id, session_id=c.claim_b.session_id, source_id=c.claim_b.source_id, dimension_id=c.claim_b.dimension_id, text=c.claim_b.claim_text, entity=c.claim_b.entity, attribute=c.claim_b.attribute, value=c.claim_b.value, claim_type=c.claim_b.claim_type, excerpt=c.claim_b.excerpt, confidence=c.claim_b.confidence, evidence_status=c.claim_b.evidence_status, freshness=c.claim_b.freshness),
            conflict_type=c.conflict_type,
            resolution_action=c.resolution_action,
        )
        for c in conflicts
    ]


@router.get("/{session_id}/checklist", response_model=List[VerificationTaskResponse])
async def get_checklist(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get verification checklist."""
    from app.models.database import ChecklistItem
    from app.schemas.research import VerificationTaskResponse
    from sqlalchemy import select
    
    result = await db.execute(
        select(ChecklistItem).where(ChecklistItem.session_id == session_id)
    )
    items = result.scalars().all()
    
    return [
        VerificationTaskResponse(
            id=c.id,
            session_id=c.session_id,
            dimension_id=c.dimension_id,
            title=c.title,
            priority=c.priority,
            explanation=c.explanation,
            completed=c.completed,
            recommended_authority=c.recommended_authority,
            verification_method=c.verification_method,
            source_ids=c.source_ids or [],
        )
        for c in items
    ]


@router.patch("/{session_id}/checklist/{task_id}", response_model=VerificationTaskResponse)
async def update_checklist_task(
    session_id: str,
    task_id: str,
    payload: ChecklistUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update checklist task completion status."""
    from app.models.database import ChecklistItem
    from sqlalchemy import update, select
    from app.schemas.research import VerificationTaskResponse
    
    result = await db.execute(
        select(ChecklistItem).where(
            ChecklistItem.id == task_id,
            ChecklistItem.session_id == session_id,
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.execute(
        update(ChecklistItem)
        .where(ChecklistItem.id == task_id)
        .values(completed=payload.completed)
    )
    await db.commit()
    
    return VerificationTaskResponse(
        id=task.id,
        session_id=task.session_id,
        dimension_id=task.dimension_id,
        title=task.title,
        priority=task.priority,
        explanation=task.explanation,
        completed=payload.completed,
        recommended_authority=task.recommended_authority,
        verification_method=task.verification_method,
        source_ids=task.source_ids or [],
    )
