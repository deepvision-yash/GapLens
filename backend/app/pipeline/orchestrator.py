import asyncio
import json
import re
import structlog
from datetime import datetime
from typing import Dict, Any, List, Optional, AsyncGenerator
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.database import (
    ResearchSession, Source, SourceChunk, Claim, Gap, Conflict, ChecklistItem
)
from app.schemas.research import (
    SessionStatus, ResearchGoal, ResearchDimension, SourceType,
    FindingStatus, CoverageStatus, Priority, ConflictType
)
from app.services.external import tavily_service, jina_service, llm_service
from app.core.config import settings
from app.core.database import AsyncSessionLocal

logger = structlog.get_logger()
ACTIVE_PIPELINE_PROGRESS: Dict[str, Dict[str, Any]] = {}


class PipelineOrchestrator:
    """Orchestrates the research pipeline with stage-by-stage execution and SSE progress."""
    
    STAGES = [
        ("understanding", "Goal Understanding"),
        ("dimensions", "Research Dimensions"),
        ("scope_review", "Scope Review"),
        ("query_planning", "Query Planning"),
        ("searching", "Web Search"),
        ("extracting", "Content Extraction"),
        ("chunking", "Chunking & Embedding"),
        ("claims", "Claim Extraction"),
        ("coverage", "Coverage Analysis"),
        ("contradictions", "Contradiction Detection"),
        ("freshness", "Freshness Analysis"),
        ("evidence", "Evidence Validation"),
        ("gaps", "Gap Prioritization"),
        ("checklist", "Verification Checklist"),
    ]
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.session_id: Optional[str] = None
        self.current_stage_index = 0
        self.partial_errors: List[str] = []
    
    async def run_pipeline(self, session_id: str) -> None:
        """Run the full research pipeline for a session."""
        self.session_id = session_id
        
        try:
            # /understand and /scope have already completed the user's review checkpoint.
            # Run only the costly research stages after POST /start transitions the session to READY.
            session = await self._get_session()
            goal = ResearchGoal(**session.goal_json)
            dimensions = [ResearchDimension(**d) for d in session.dimensions_json]
            await self._emit_progress("query_planning", 20, "Planning search queries")
            
            # Stage 4: Query Planning
            queries = await self._stage_plan_queries(goal, dimensions)
            
            # Stage 5: Parallel Web Search
            await self._update_status(SessionStatus.SEARCHING)
            await self._emit_progress("searching", 30, "Searching the web for sources")
            sources = await self._stage_search(queries)
            if not sources:
                raise RuntimeError("No real sources were found. Configure the selected search provider or add source URLs and retry.")
            await self._emit_progress("searching", 35, f"Found {len(sources)} sources")
            
            # Stage 6: Source Extraction
            await self._update_status(SessionStatus.EXTRACTING)
            await self._emit_progress("extracting", 42, "Extracting source content")
            await self._stage_extract_sources(sources)
            await self._emit_progress("extracting", 50, f"Extracted {len(sources)} sources")
            
            # Stage 7: Chunking & Embedding
            await self._emit_progress("chunking", 50, "Chunking sources and generating embeddings")
            await self._stage_chunk_and_embed(sources)
            await self._emit_progress("chunking", 55, "Chunked and embedded sources")
            
            # Stage 8: Claim Extraction
            await self._update_status(SessionStatus.CLAIM_EXTRACTION)
            await self._emit_progress("claims", 58, "Extracting source-grounded claims")
            claims = await self._stage_extract_claims(sources, dimensions)
            await self._emit_progress("claims", 65, f"Extracted {len(claims)} claims")
            
            # Stage 9: Coverage Analysis
            await self._update_status(SessionStatus.ANALYZING)
            await self._emit_progress("coverage", 66, "Analyzing dimension coverage")
            await self._stage_coverage_analysis(dimensions, claims)
            await self._emit_progress("coverage", 70, "Completed coverage analysis")
            
            # Stage 10: Contradiction Detection
            await self._emit_progress("contradictions", 70, "Checking for conflicting claims")
            conflicts = await self._stage_detect_contradictions(claims)
            await self._emit_progress("contradictions", 75, f"Found {len(conflicts)} conflicts")
            session = await self._get_session()
            dimensions = [ResearchDimension(**item) for item in session.dimensions_json]
            
            # Stage 11: Freshness Analysis
            await self._emit_progress("freshness", 75, "Checking source publication dates")
            await self._stage_freshness_analysis(sources, claims)
            await self._emit_progress("freshness", 80, "Completed freshness analysis")
            
            # Stage 12: Evidence Validation
            await self._emit_progress("evidence", 80, "Validating claim excerpts against source text")
            await self._stage_evidence_validation(claims, sources)
            await self._emit_progress("evidence", 85, "Completed evidence validation")
            
            # Stage 13: Gap Prioritization
            await self._emit_progress("gaps", 86, "Identifying research gaps")
            gaps = await self._stage_gap_prioritization(dimensions, claims)
            await self._emit_progress("gaps", 90, f"Identified {len(gaps)} gaps")
            
            # Stage 14: Verification Checklist
            await self._update_status(SessionStatus.GENERATING_CHECKLIST)
            await self._emit_progress("checklist", 93, "Building the verification checklist")
            checklist = await self._stage_verification_checklist(gaps, claims, sources)
            await self._emit_progress("checklist", 95, f"Generated {len(checklist)} verification tasks")
            
            # Complete
            partial = bool(self.partial_errors) or not sources or any(s.extraction_status != "success" for s in sources)
            await self._complete_session(is_partial=partial)
            await self._emit_progress("completed", 100, "Research completed")
            
        except Exception as e:
            logger.error("Pipeline failed", session_id=self.session_id, error=str(e))
            await self._fail_session(str(e))
    
    async def _update_status(self, status: SessionStatus) -> None:
        """Update session status in database."""
        await self.db.execute(
            update(ResearchSession)
            .where(ResearchSession.id == self.session_id)
            .values(status=status, updated_at=datetime.utcnow())
        )
        await self.db.commit()
    
    async def _get_session(self) -> ResearchSession:
        result = await self.db.execute(
            select(ResearchSession).where(ResearchSession.id == self.session_id)
        )
        return result.scalar_one()
    
    async def _emit_progress(self, stage: str, progress: Optional[int], message: str) -> None:
        """Emit progress event (stored for SSE polling)."""
        # In a real implementation, this would push to Redis or in-memory store
        # For now, we update the session with progress info
        await self.db.execute(
            update(ResearchSession)
            .where(ResearchSession.id == self.session_id)
            .values(
                updated_at=datetime.utcnow(),
            )
        )
        await self.db.commit()
        stage_names = [key for key, _ in self.STAGES]
        if stage == "completed":
            completed = stage_names
            pending = []
        else:
            current_index = stage_names.index(stage) if stage in stage_names else 0
            completed = stage_names[:current_index]
            pending = stage_names[current_index + 1:]
        ACTIVE_PIPELINE_PROGRESS[self.session_id] = {
            "current_stage": stage,
            "current_message": message,
            "stages_completed": completed,
            "stages_pending": pending,
            "progress": progress,
        }
        logger.info("Pipeline progress", session_id=self.session_id, stage=stage, progress=progress, message=message)
    
    # Pipeline Stages
    
    async def _stage_understand_goal(self) -> ResearchGoal:
        """Stage 1: Understand the research goal using LLM."""
        session = await self._get_session()
        goal_data = session.goal_json
        
        prompt = f"""
        Analyze this research query and extract structured understanding:
        
        Query: {session.goal_text}
        
        Return JSON with:
        - original_query: string
        - interpreted_objective: string (clear, actionable research objective)
        - entities: array of strings (key entities, programs, organizations)
        - scope: array of strings (what's in/out of scope)
        - geography: array of strings (countries, states, regions)
        - time_constraints: string (deadlines, cycles, years; omit when none are specified)
        - constraints: array of strings (budget, eligibility, format requirements)
        """
        
        schema = {
            "type": "object",
            "properties": {
                "original_query": {"type": "string"},
                "interpreted_objective": {"type": "string"},
                "entities": {"type": "array", "items": {"type": "string"}},
                "scope": {"type": "array", "items": {"type": "string"}},
                "geography": {"type": "array", "items": {"type": "string"}},
                # Gemini's legacy responseSchema endpoint rejects nullable
                # union types. This field is optional in the schema, so an
                # omitted value maps to ResearchGoal.time_constraints=None.
                "time_constraints": {"type": "string"},
                "constraints": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["original_query", "interpreted_objective", "entities", "scope", "geography", "constraints"],
        }
        
        result = await llm_service.generate_structured(prompt, schema)
        if not isinstance(result, dict):
            raise ValueError("The LLM returned invalid research understanding.")
        # The input goal belongs to this session and is authoritative. Never
        # let model-generated text replace it in the saved session response.
        result["original_query"] = session.goal_text
        
        goal = ResearchGoal(**result)
        
        # Update session with goal understanding
        await self.db.execute(
            update(ResearchSession)
            .where(ResearchSession.id == self.session_id)
            .values(goal_json=result)
        )
        await self.db.commit()
        
        return goal
    
    async def _stage_generate_dimensions(self, goal: ResearchGoal) -> List[ResearchDimension]:
        """Stage 2: Generate research dimensions."""
        prompt = f"""
        Based on this research goal, generate between 4 and 6 specific research dimensions. Never return more than 6:
        
        Goal: {goal.interpreted_objective}
        Entities: {goal.entities}
        Scope: {goal.scope}
        Geography: {goal.geography}
        Time: {goal.time_constraints}
        
        Return JSON array of dimensions, each with:
        - id: unique string
        - name: short dimension name
        - description: what this dimension investigates
        - questions: array of specific questions to answer
        - priority: 1-5 (5 = critical)
        """
        
        schema = {
            "type": "array",
            "maxItems": settings.MAX_DIMENSIONS,
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "questions": {"type": "array", "items": {"type": "string"}},
                    "priority": {"type": "integer", "minimum": 1, "maximum": 5},
                },
                "required": ["id", "name", "description", "questions", "priority"],
            },
        }
        
        result = await llm_service.generate_structured(prompt, schema)
        if not isinstance(result, list):
            raise ValueError("The LLM returned invalid research dimensions.")
        generated = [ResearchDimension(**d) for d in result]
        generated = generated[:settings.MAX_DIMENSIONS]
        session = await self._get_session()
        custom = [ResearchDimension(**d) for d in session.dimensions_json]
        generated_names = {dimension.name.casefold() for dimension in generated}
        dimensions = (generated + [d for d in custom if d.name.casefold() not in generated_names])[:settings.MAX_DIMENSIONS]
        if not dimensions:
            raise ValueError("No research dimensions were generated. Retry scope generation.")
        if len({dimension.id for dimension in dimensions}) != len(dimensions):
            raise ValueError("Research dimensions contain duplicate IDs. Retry scope generation.")
        
        # Store dimensions
        dims_json = [d.model_dump() for d in dimensions]
        await self.db.execute(
            update(ResearchSession)
            .where(ResearchSession.id == self.session_id)
            .values(dimensions_json=dims_json)
        )
        await self.db.commit()
        
        return dimensions
    
    async def _stage_plan_queries(self, goal: ResearchGoal, dimensions: List[ResearchDimension]) -> List[str]:
        """Plan targeted searches for every scope dimension in one model request."""
        dimension_specs = [
            {"id": dim.id, "name": dim.name, "description": dim.description, "questions": dim.questions}
            for dim in dimensions
        ]
        prompt = f"""
        Plan two focused web search queries for each research dimension below.
        Queries must seek verifiable information, prefer official or primary sources where applicable,
        and include relevant geography or time constraints from the research objective.

        Objective: {goal.interpreted_objective}
        Geography: {goal.geography}
        Time constraints: {goal.time_constraints}
        Dimensions: {json.dumps(dimension_specs, ensure_ascii=False)}

        Return one object per dimension containing its exact dimension_id and an array of search queries.
        Do not invent findings or report results; this is query planning only.
        """
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "dimension_id": {"type": "string"},
                    "queries": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["dimension_id", "queries"],
            },
        }
        result = await llm_service.generate_structured(prompt, schema)
        if not isinstance(result, list):
            raise RuntimeError("Query planning returned an invalid response.")
        known = {dim.id for dim in dimensions}
        queries = [
            value.strip()
            for item in result if isinstance(item, dict) and item.get("dimension_id") in known
            for value in item.get("queries", []) if isinstance(value, str) and value.strip()
        ]
        if not queries:
            raise RuntimeError("Query planning did not produce any usable search queries.")
        return list(dict.fromkeys(queries))
    
    async def _stage_search(self, queries: List[str]) -> List[Source]:
        """Stage 5: Parallel web search using Tavily."""
        # Include URL sources supplied during session creation in the same extraction pipeline.
        initial = await self.db.execute(select(Source).where(Source.session_id == self.session_id))
        sources = list(initial.scalars().all())
        known_urls = {source.url for source in sources if source.url}

        provider = settings.SEARCH_PROVIDER.strip().lower()
        search_ready = bool(settings.JINA_API_KEY) if provider == "jina" else bool(settings.TAVILY_API_KEY)
        if provider not in {"jina", "tavily"}:
            raise RuntimeError("SEARCH_PROVIDER must be either 'jina' or 'tavily'.")
        if not search_ready:
            message = f"{provider} web search is not configured; only user-submitted URLs can be processed."
            if not sources:
                raise RuntimeError(f"{message} Add {provider.upper()} credentials or submit a source URL.")
            self.partial_errors.append(message)
            return sources
        
        # Deduplicate queries
        unique_queries = list(dict.fromkeys(queries))
        
        for query in unique_queries:
            remaining = settings.MAX_SOURCES_PER_SESSION - len(sources)
            if remaining <= 0:
                break
            try:
                result = await tavily_service.search(
                    query=query,
                    max_results=min(3, remaining),
                    search_depth=settings.SEARCH_DEPTH,
                )
            except Exception as exc:
                self.partial_errors.append(str(exc))
                logger.warning("Search query failed; continuing with remaining sources", query=query, error=str(exc))
                continue
            
            for item in result.get("results", []):
                url = item.get("url", "")
                if not url or url in known_urls:
                    continue
                source = Source(
                    id=str(uuid4()),
                    session_id=self.session_id,
                    url=url,
                    title=item.get("title", ""),
                    domain=self._extract_domain(item.get("url", "")),
                    source_type=self._classify_source_type(item.get("url", "")),
                    publication_date=self._parse_date(item.get("published_date")),
                    relevance_score=item.get("score", 0.0),
                    extraction_status="pending",
                )
                self.db.add(source)
                sources.append(source)
                known_urls.add(url)
                if len(sources) >= settings.MAX_SOURCES_PER_SESSION:
                    break
        
        await self.db.commit()
        return sources
    
    async def _stage_extract_sources(self, sources: List[Source]) -> None:
        """Stage 6: Extract content from sources using Jina Reader."""
        for source in sources:
            if not source.url:
                # Uploaded documents were parsed and persisted by the upload endpoint.
                if source.content and source.extraction_status == "success":
                    continue
                source.extraction_status = "failed"
                continue
            
            try:
                result = await jina_service.extract(source.url)
                
                if result.get("success") and result.get("content", "").strip():
                    extracted = result.get("content", "")
                    title = result.get("title", source.title)
                    access_challenge_markers = (
                        "checking your browser", "recaptcha", "captcha challenge",
                        "verify you are human", "access denied", "cloudflare ray id",
                    )
                    opening_text = f"{title or ''}\n{extracted[:600]}".casefold()
                    if any(marker in opening_text for marker in access_challenge_markers):
                        source.extraction_status = "failed"
                        self.partial_errors.append(f"Source extraction returned an access challenge for {source.url}.")
                        continue
                    source.content = extracted
                    source.title = title
                    source.extraction_status = "success"
                else:
                    source.extraction_status = "failed"
                    self.partial_errors.append(f"Source extraction failed for {source.url}: {result.get('error', 'no content returned')}")
            except Exception as e:
                logger.error("Extraction failed", source_id=source.id, error=str(e))
                source.extraction_status = "failed"
                self.partial_errors.append(f"Source extraction failed for {source.url}: {e}")
        
        await self.db.commit()
    
    async def _stage_chunk_and_embed(self, sources: List[Source]) -> None:
        """Stage 7: Chunk sources and store Jina embeddings for semantic retrieval."""
        pending_chunks = []
        for source in sources:
            if not source.content or source.extraction_status != "success":
                continue
            
            chunks = self._chunk_text(source.content, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
            
            for i, chunk in enumerate(chunks):
                chunk_obj = SourceChunk(
                    id=str(uuid4()),
                    source_id=source.id,
                    chunk_index=i,
                    content=chunk,
                    token_count=len(chunk.split()),
                    embedding=None,
                    char_start=i * (settings.CHUNK_SIZE - settings.CHUNK_OVERLAP),
                    char_end=(i + 1) * settings.CHUNK_SIZE,
                )
                self.db.add(chunk_obj)
                pending_chunks.append(chunk_obj)

        if pending_chunks and settings.JINA_API_KEY:
            try:
                texts = [chunk.content for chunk in pending_chunks]
                vectors = []
                for offset in range(0, len(texts), 32):
                    vectors.extend(await jina_service.embed(texts[offset:offset + 32]))
                for chunk, vector in zip(pending_chunks, vectors):
                    chunk.embedding = vector
            except Exception as exc:
                self.partial_errors.append(f"Chunk embeddings unavailable: {exc}")
                logger.warning("Embedding stage incomplete", error=str(exc))
        elif pending_chunks:
            self.partial_errors.append("Chunk embeddings skipped because JINA_API_KEY is not configured.")
        
        await self.db.commit()
    
    async def _stage_extract_claims(
        self, sources: List[Source], dimensions: List[ResearchDimension]
    ) -> List[Claim]:
        """Stage 8: Extract source-grounded claims with one model call per source."""
        claims = []
        dim_map = {d.id: d for d in dimensions}
        dimension_specs = [
            {"id": d.id, "name": d.name, "description": d.description[:240]}
            for d in dimensions
        ]
        
        for source in sources:
            if not source.content or source.extraction_status != "success":
                continue
            prompt = f"""
            Extract only factual claims supported by the supplied source text.
            Assign each claim to the most relevant dimension using its exact id below.
            Copy each excerpt verbatim from the source; never paraphrase or invent a citation.
            Ignore claims that cannot be tied to an exact source passage.

            Source reference: {source.url or source.title or source.id}
            Source title: {source.title}
            Research dimensions: {json.dumps(dimension_specs, ensure_ascii=False)}
            Source content (first 6000 characters):
            {source.content[:6000]}

            Return at most 3 high-value JSON claims for this source. Keep entity, attribute,
            value, and claim_type concise. Copy an exact excerpt of at most 400 characters.
            Include dimension_id and confidence from 0 to 1.
            """
            schema = {
                "type": "array",
            "maxItems": 3,
                "items": {
                    "type": "object",
                    "properties": {
                    "dimension_id": {"type": "string"},
                    "entity": {"type": "string"},
                    "attribute": {"type": "string"},
                    "value": {"type": "string"},
                    "claim_type": {"type": "string"},
                    "excerpt": {"type": "string"},
                        "confidence": {"type": "number"},
                    },
                    "required": ["dimension_id", "entity", "attribute", "value", "claim_type", "excerpt", "confidence"],
                },
            }
            try:
                result = await llm_service.generate_structured(prompt, schema)
            except Exception as exc:
                self.partial_errors.append(f"Claim extraction failed for {source.url}: {exc}")
                logger.warning("Claim extraction failed for source", source_id=source.id, error=str(exc))
                continue
            if not isinstance(result, list):
                self.partial_errors.append(f"Claim extraction returned invalid data for {source.url}.")
                continue

            for claim_data in result:
                if not isinstance(claim_data, dict) or not all(claim_data.get(key) for key in (
                    "dimension_id", "entity", "attribute", "value", "claim_type", "excerpt"
                )):
                    self.partial_errors.append(f"Claim extraction returned an incomplete claim for {source.url}.")
                    continue
                dimension = dim_map.get(claim_data["dimension_id"])
                if not dimension:
                    self.partial_errors.append(f"Claim extraction returned an unknown dimension for {source.url}.")
                    continue
                confidence = claim_data.get("confidence", 0.0)
                if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
                    confidence = 0.0
                confidence = max(0.0, min(1.0, float(confidence)))
                claim = Claim(
                    id=str(uuid4()),
                    session_id=self.session_id,
                    source_id=source.id,
                    dimension_id=dimension.id,
                    claim_text=f"{claim_data['entity']} {claim_data['attribute']} is {claim_data['value']}",
                    entity=claim_data["entity"],
                    attribute=claim_data["attribute"],
                    value=claim_data["value"],
                    claim_type=claim_data["claim_type"],
                    excerpt=claim_data["excerpt"],
                    confidence=confidence,
                    evidence_status=FindingStatus.UNVERIFIED,
                )
                self.db.add(claim)
                claims.append(claim)
        
        await self.db.commit()
        return claims
    
    async def _stage_coverage_analysis(
        self, dimensions: List[ResearchDimension], claims: List[Claim]
    ) -> None:
        """Stage 9: Analyze coverage per dimension."""
        claims_by_dim = {}
        for claim in claims:
            claims_by_dim.setdefault(claim.dimension_id, []).append(claim)
        
        for dim in dimensions:
            dim_claims = claims_by_dim.get(dim.id, [])
            
            if not dim_claims:
                dim.coverage_status = CoverageStatus.MISSING
            elif len({claim.source_id for claim in dim_claims}) >= 2 and len(dim_claims) >= max(1, len(dim.questions)):
                dim.coverage_status = CoverageStatus.COVERED
            else:
                dim.coverage_status = CoverageStatus.PARTIAL
            
            dim.claim_count = len(dim_claims)
        
        # Update dimensions in session
        session = await self._get_session()
        dims_json = [d.model_dump() for d in dimensions]
        await self.db.execute(
            update(ResearchSession)
            .where(ResearchSession.id == self.session_id)
            .values(dimensions_json=dims_json)
        )
        await self.db.commit()
    
    async def _stage_detect_contradictions(self, claims: List[Claim]) -> List[Conflict]:
        """Stage 10: Detect contradictions between claims."""
        conflicts = []
        
        # Group claims by entity+attribute
        claim_groups = {}
        for claim in claims:
            key = (claim.entity.lower(), claim.attribute.lower())
            claim_groups.setdefault(key, []).append(claim)
        
        conflicting_dimensions = set()
        for (entity, attr), group in claim_groups.items():
            if len(group) < 2:
                continue
            
            # Require distinct source records and differing values before surfacing a conflict.
            distinct_claims = {}
            for claim in group:
                distinct_claims.setdefault(claim.value.strip().casefold(), claim)
            pair = next(
                ((left, right) for left in distinct_claims.values() for right in distinct_claims.values()
                 if left.id != right.id and left.source_id != right.source_id),
                None,
            )
            if pair:
                c1, c2 = pair
                conflict = Conflict(
                    id=str(uuid4()),
                    session_id=self.session_id,
                    entity=c1.entity,
                    attribute=c1.attribute,
                    claim_a_id=c1.id,
                    claim_b_id=c2.id,
                    conflict_type=ConflictType.UNCERTAIN,
                    resolution_action=f"Verify {entity} {attr} on official source",
                    confidence=min(c1.confidence, c2.confidence),
                )
                self.db.add(conflict)
                conflicts.append(conflict)
                conflicting_dimensions.update((c1.dimension_id, c2.dimension_id))

        if conflicting_dimensions:
            session = await self._get_session()
            dimensions = [ResearchDimension(**item) for item in session.dimensions_json]
            for dimension in dimensions:
                if dimension.id in conflicting_dimensions:
                    dimension.coverage_status = CoverageStatus.CONFLICTING
            await self.db.execute(
                update(ResearchSession)
                .where(ResearchSession.id == self.session_id)
                .values(dimensions_json=[dimension.model_dump() for dimension in dimensions])
            )
        
        await self.db.commit()
        return conflicts
    
    async def _stage_freshness_analysis(self, sources: List[Source], claims: List[Claim]) -> None:
        """Attach source publication dates when available; do not infer an age rating."""
        publication_dates = {
            source.id: source.publication_date.date().isoformat()
            for source in sources if source.publication_date
        }
        for claim in claims:
            published = publication_dates.get(claim.source_id)
            if published:
                claim.freshness = f"Source publication date: {published}"
        await self.db.commit()
    
    async def _stage_evidence_validation(self, claims: List[Claim], sources: List[Source]) -> None:
        """Stage 12: Require each claimed excerpt to occur in its cited source."""
        source_map = {s.id: s for s in sources}
        
        for claim in claims:
            source = source_map.get(claim.source_id)
            if not source or not source.content:
                claim.evidence_status = FindingStatus.UNVERIFIED
                continue

            excerpt = re.sub(r"[^\w]+", " ", (claim.excerpt or "").casefold(), flags=re.UNICODE).strip()
            source_text = re.sub(r"[^\w]+", " ", source.content.casefold(), flags=re.UNICODE)
            if excerpt and excerpt in source_text:
                # A matched passage supports traceability, not truth; verification remains a separate task.
                claim.evidence_status = FindingStatus.POTENTIAL
            else:
                claim.evidence_status = FindingStatus.UNVERIFIED
                self.partial_errors.append(f"Claim excerpt could not be matched to source {source.url or source.title or source.id}.")
        
        await self.db.commit()
    
    async def _stage_gap_prioritization(
        self, dimensions: List[ResearchDimension], claims: List[Claim]
    ) -> List[Gap]:
        """Stage 13: Prioritize information gaps."""
        gaps = []
        claims_by_dim = {}
        for claim in claims:
            claims_by_dim.setdefault(claim.dimension_id, []).append(claim)
        
        for dim in dimensions:
            dim_claims = claims_by_dim.get(dim.id, [])
            
            if not dim_claims:
                gap = Gap(
                    id=str(uuid4()),
                    session_id=self.session_id,
                    dimension_id=dim.id,
                    title=f"Missing: {dim.name}",
                    explanation=f"No claims found for {dim.description}",
                    priority=Priority.CRITICAL if dim.priority >= 4 else Priority.HIGH,
                    evidence_summary="No sources addressed this dimension",
                    next_action=f"Search for {dim.name} on official portals",
                    recommended_authority="Official government portal",
                    verification_method="official_source",
                    source_ids=[],
                )
                self.db.add(gap)
                gaps.append(gap)
            elif dim.coverage_status == CoverageStatus.CONFLICTING:
                gap = Gap(
                    id=str(uuid4()),
                    session_id=self.session_id,
                    dimension_id=dim.id,
                    title=f"Conflict: {dim.name}",
                    explanation=f"Conflicting claims found for {dim.name}",
                    priority=Priority.CRITICAL,
                    evidence_summary=" | ".join(dict.fromkeys(c.excerpt for c in dim_claims if c.excerpt))[:1200],
                    next_action="Compare the cited source passages and confirm the current value with an authoritative source",
                    recommended_authority="Official portal",
                    verification_method="cross_reference",
                    source_ids=list(dict.fromkeys(c.source_id for c in dim_claims)),
                )
                self.db.add(gap)
                gaps.append(gap)
        
        await self.db.commit()
        return gaps
    
    async def _stage_verification_checklist(
        self, gaps: List[Gap], claims: List[Claim], sources: List[Source]
    ) -> List[ChecklistItem]:
        """Stage 14: Generate verification checklist."""
        checklist = []
        
        for gap in gaps:
            item = ChecklistItem(
                id=str(uuid4()),
                session_id=self.session_id,
                dimension_id=gap.dimension_id,
                title=gap.next_action,
                priority=gap.priority,
                explanation=gap.explanation,
                completed=False,
                recommended_authority=gap.recommended_authority,
                verification_method=gap.verification_method,
                source_ids=gap.source_ids or [],
            )
            self.db.add(item)
            checklist.append(item)
        
        await self.db.commit()
        return checklist
    
    async def _complete_session(self, is_partial: bool = False) -> None:
        """Mark session as completed."""
        await self.db.execute(
            update(ResearchSession)
            .where(ResearchSession.id == self.session_id)
            .values(
                status=SessionStatus.PARTIAL if is_partial else SessionStatus.COMPLETED,
                is_partial=is_partial,
                error="; ".join(self.partial_errors[:10]) if self.partial_errors else None,
                completed_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
        await self.db.commit()
    
    async def _fail_session(self, error: str) -> None:
        """Mark session as failed."""
        await self.db.rollback()
        await self.db.execute(
            update(ResearchSession)
            .where(ResearchSession.id == self.session_id)
            .values(
                status=SessionStatus.FAILED,
                error=error,
                updated_at=datetime.utcnow(),
            )
        )
        await self.db.commit()
    
    # Helper methods
    
    def _extract_domain(self, url: str) -> str:
        from urllib.parse import urlparse
        try:
            return urlparse(url).netloc
        except:
            return "unknown"
    
    def _classify_source_type(self, url: str) -> SourceType:
        domain = self._extract_domain(url).lower()
        
        if any(d in domain for d in [".gov.in", ".nic.in", "gov."]):
            return SourceType.OFFICIAL_GOVERNMENT
        if any(d in domain for d in [".edu", ".ac.in"]):
            return SourceType.ACADEMIC
        if any(d in domain for d in ["rbi.org.in", "sebi.gov.in", "irdai.gov.in"]):
            return SourceType.REGULATORY
        if any(d in domain for d in ["nsp.gov.in", "scholarships.gov.in"]):
            return SourceType.OFFICIAL_PORTAL
        return SourceType.GENERAL
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y", "%B %d, %Y"]:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue
        return None
    
    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks


async def run_pipeline(session_id: str) -> None:
    """Run a session with a task-owned database session, independent of the request."""
    async with AsyncSessionLocal() as db:
        orchestrator = PipelineOrchestrator(db)
        await orchestrator.run_pipeline(session_id)
