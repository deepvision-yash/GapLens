from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from sse_starlette.sse import EventSourceResponse
import asyncio
import json

from app.core.database import get_db
from app.models.database import ResearchSession
from app.schemas.research import (
    ResearchSessionCreate, ResearchSessionResponse, ResearchScopeResponse,
    DimensionUpdate, SourceCreate, SourceResponse,
    SessionStatusResponse, SessionStatus, ResearchResultsResponse,
    ChecklistUpdate, VerificationTaskResponse,
)
from app.pipeline.orchestrator import run_pipeline

router = APIRouter(prefix="/api/research", tags=["research"])


@router.post("", response_model=ResearchSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_research(
    payload: ResearchSessionCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new research session."""
    session = ResearchSession(
        goal_text=payload.goal,
        goal_json={"original_query": payload.goal},
        dimensions_json=[],
        status=SessionStatus.CREATED,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    return ResearchSessionResponse(
        id=session.id,
        goal=session.goal_text,
        status=session.status,
        created_at=session.created_at,
        updated_at=session.updated_at,
        source_count=0,
        dimension_count=0,
    )


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
    
    # Import here to avoid circular imports
    from app.pipeline.orchestrator import PipelineOrchestrator
    
    orchestrator = PipelineOrchestrator(db)
    orchestrator.session_id = session_id
    
    # Run understanding and dimension generation
    goal = await orchestrator._stage_understand_goal()
    dimensions = await orchestrator._stage_generate_dimensions(goal)
    
    # Update status to scope_review
    from app.schemas.research import SessionStatus
    from sqlalchemy import update
    from datetime import datetime
    
    await db.execute(
        update(ResearchSession)
        .where(ResearchSession.id == session_id)
        .values(status=SessionStatus.SCOPE_REVIEW, updated_at=datetime.utcnow())
    )
    await db.commit()
    
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
    
    dims_json = [d.model_dump() for d in payload.dimensions]
    
    await db.execute(
        update(ResearchSession)
        .where(ResearchSession.id == session_id)
        .values(dimensions_json=dims_json, updated_at=datetime.utcnow())
    )
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
    from app.schemas.research import SessionStatus
    
    result = await db.execute(
        select(ResearchSession).where(ResearchSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.status != SessionStatus.SCOPE_REVIEW:
        raise HTTPException(status_code=400, detail="Session not in scope_review state")
    
    # Update status to READY (pipeline will pick up)
    await db.execute(
        update(ResearchSession)
        .where(ResearchSession.id == session_id)
        .values(status=SessionStatus.READY, updated_at=datetime.utcnow())
    )
    await db.commit()
    
    # Start pipeline in background
    background_tasks.add_task(run_pipeline, session_id, db)
    
    return {"message": "Research started", "session_id": session_id}


@router.get("/{session_id}/events")
async def sse_events(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """SSE endpoint for real-time progress updates."""
    
    async def event_generator():
        last_update = None
        while True:
            result = await db.execute(
                select(ResearchSession).where(ResearchSession.id == session_id)
            )
            session = result.scalar_one_or_none()
            
            if not session:
                yield {"event": "error", "data": json.dumps({"error": "Session not found"})}
                break
            
            # Check for updates
            current_update = session.updated_at
            if current_update != last_update:
                last_update = current_update
                
                data = {
                    "session_id": session_id,
                    "status": session.status.value,
                    "updated_at": session.updated_at.isoformat() if session.updated_at else None,
                }
                yield {"event": "progress", "data": json.dumps(data)}
            
            # Check for completion
            if session.status in [SessionStatus.COMPLETED, SessionStatus.FAILED, SessionStatus.PARTIAL]:
                yield {"event": "complete", "data": json.dumps({"status": session.status.value})}
                break
            
            await asyncio.sleep(1)
    
    return EventSourceResponse(event_generator())


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
    
    # Map status to progress
    progress_map = {
        SessionStatus.CREATED: 0,
        SessionStatus.UNDERSTANDING: 5,
        SessionStatus.SCOPE_REVIEW: 15,
        SessionStatus.READY: 20,
        SessionStatus.SEARCHING: 30,
        SessionStatus.EXTRACTING: 45,
        SessionStatus.CLAIM_EXTRACTION: 60,
        SessionStatus.ANALYZING: 70,
        SessionStatus.GENERATING_CHECKLIST: 90,
        SessionStatus.COMPLETED: 100,
        SessionStatus.PARTIAL: 100,
        SessionStatus.FAILED: 0,
    }
    
    stages = [
        "understanding", "dimensions", "scope_review", "query_planning",
        "searching", "extracting", "chunking", "claims",
        "coverage", "contradictions", "freshness", "evidence",
        "gaps", "checklist",
    ]
    
    completed_idx = stages.index("scope_review") if session.status == SessionStatus.SCOPE_REVIEW else 0
    if session.status == SessionStatus.COMPLETED:
        completed_idx = len(stages)
    
    return SessionStatusResponse(
        session_id=session_id,
        status=session.status,
        current_stage=session.status.value,
        progress=progress_map.get(session.status, 0),
        stages_completed=stages[:completed_idx],
        stages_pending=stages[completed_idx:],
        sources_found=source_count or 0,
        claims_extracted=claim_count or 0,
        errors=[session.error] if session.error else [],
        is_partial=session.is_partial,
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
    
    conflicts_result = await db.execute(
        select(Conflict).where(Conflict.session_id == session_id)
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


@router.get("/{session_id}/claims", response_model=List)
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


@router.get("/{session_id}/gaps", response_model=List)
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
        }
        for g in gaps
    ]


@router.get("/{session_id}/conflicts", response_model=List)
async def get_conflicts(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get all conflicts for a session."""
    from app.models.database import Conflict
    from sqlalchemy import select
    
    result = await db.execute(
        select(Conflict).where(Conflict.session_id == session_id)
    )
    conflicts = result.scalars().all()
    
    return [
        {
            "id": c.id,
            "session_id": c.session_id,
            "entity": c.entity,
            "attribute": c.attribute,
            "conflict_type": c.conflict_type.value,
            "resolution_action": c.resolution_action,
            "confidence": c.confidence,
        }
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