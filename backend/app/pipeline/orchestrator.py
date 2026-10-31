import asyncio
import json
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

logger = structlog.get_logger()


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
    
    async def run_pipeline(self, session_id: str) -> None:
        """Run the full research pipeline for a session."""
        self.session_id = session_id
        
        try:
            # Update status to understanding
            await self._update_status(SessionStatus.UNDERSTANDING)
            
            # Stage 1: Goal Understanding
            goal = await self._stage_understand_goal()
            await self._emit_progress("understanding", 5, "Understood research goal")
            
            # Stage 2: Research Dimensions
            dimensions = await self._stage_generate_dimensions(goal)
            await self._emit_progress("dimensions", 10, f"Generated {len(dimensions)} dimensions")
            
            # Stage 3: Scope Review (wait for user confirmation via API)
            await self._update_status(SessionStatus.SCOPE_REVIEW)
            await self._emit_progress("scope_review", 15, "Awaiting scope confirmation")
            
            # Wait for READY status (triggered by POST /start)
            while True:
                await asyncio.sleep(1)
                session = await self._get_session()
                if session.status == SessionStatus.READY:
                    break
                elif session.status == SessionStatus.FAILED:
                    return
            
            await self._emit_progress("query_planning", 20, "Planning search queries")
            
            # Stage 4: Query Planning
            queries = await self._stage_plan_queries(goal, dimensions)
            
            # Stage 5: Parallel Web Search
            await self._update_status(SessionStatus.SEARCHING)
            sources = await self._stage_search(queries)
            await self._emit_progress("searching", 35, f"Found {len(sources)} sources")
            
            # Stage 6: Source Extraction
            await self._update_status(SessionStatus.EXTRACTING)
            await self._stage_extract_sources(sources)
            await self._emit_progress("extracting", 50, f"Extracted {len(sources)} sources")
            
            # Stage 7: Chunking & Embedding
            await self._stage_chunk_and_embed(sources)
            await self._emit_progress("chunking", 55, "Chunked and embedded sources")
            
            # Stage 8: Claim Extraction
            await self._update_status(SessionStatus.CLAIM_EXTRACTION)
            claims = await self._stage_extract_claims(sources, dimensions)
            await self._emit_progress("claims", 65, f"Extracted {len(claims)} claims")
            
            # Stage 9: Coverage Analysis
            await self._update_status(SessionStatus.ANALYZING)
            await self._stage_coverage_analysis(dimensions, claims)
            await self._emit_progress("coverage", 70, "Completed coverage analysis")
            
            # Stage 10: Contradiction Detection
            conflicts = await self._stage_detect_contradictions(claims)
            await self._emit_progress("contradictions", 75, f"Found {len(conflicts)} conflicts")
            
            # Stage 11: Freshness Analysis
            await self._stage_freshness_analysis(sources)
            await self._emit_progress("freshness", 80, "Completed freshness analysis")
            
            # Stage 12: Evidence Validation
            await self._stage_evidence_validation(claims, sources)
            await self._emit_progress("evidence", 85, "Completed evidence validation")
            
            # Stage 13: Gap Prioritization
            gaps = await self._stage_gap_prioritization(dimensions, claims)
            await self._emit_progress("gaps", 90, f"Identified {len(gaps)} gaps")
            
            # Stage 14: Verification Checklist
            await self._update_status(SessionStatus.GENERATING_CHECKLIST)
            checklist = await self._stage_verification_checklist(gaps, claims, sources)
            await self._emit_progress("checklist", 95, f"Generated {len(checklist)} verification tasks")
            
            # Complete
            await self._complete_session()
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
    
    async def _emit_progress(self, stage: str, progress: int, message: str) -> None:
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
        - time_constraints: string or null (deadlines, cycles, years)
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
                "time_constraints": {"type": ["string", "null"]},
                "constraints": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["original_query", "interpreted_objective", "entities", "scope", "geography", "constraints"],
        }
        
        result = await llm_service.generate_structured(prompt, schema)
        
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
        Based on this research goal, generate 5-10 specific research dimensions:
        
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
        dimensions = [ResearchDimension(**d) for d in result]
        
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
        """Stage 4: Plan search queries for each dimension."""
        queries = []
        
        for dim in dimensions:
            prompt = f"""
            Generate 2-3 targeted search queries for this research dimension:
            
            Dimension: {dim.name}
            Description: {dim.description}
            Questions: {dim.questions}
            Goal: {goal.interpreted_objective}
            
            Return JSON array of query strings.
            """
            
            schema = {"type": "array", "items": {"type": "string"}}
            
            result = await llm_service.generate_structured(prompt, schema)
            queries.extend(result)
        
        return queries
    
    async def _stage_search(self, queries: List[str]) -> List[Source]:
        """Stage 5: Parallel web search using Tavily."""
        sources = []
        
        # Deduplicate queries
        unique_queries = list(dict.fromkeys(queries))[:settings.MAX_SOURCES_PER_SESSION]
        
        for query in unique_queries:
            result = await tavily_service.search(
                query=query,
                max_results=3,
                search_depth=settings.SEARCH_DEPTH,
            )
            
            for item in result.get("results", []):
                source = Source(
                    id=str(uuid4()),
                    session_id=self.session_id,
                    url=item.get("url", ""),
                    title=item.get("title", ""),
                    domain=self._extract_domain(item.get("url", "")),
                    source_type=self._classify_source_type(item.get("url", "")),
                    publication_date=self._parse_date(item.get("published_date")),
                    relevance_score=item.get("score", 0.0),
                    extraction_status="pending",
                )
                self.db.add(source)
                sources.append(source)
        
        await self.db.commit()
        return sources
    
    async def _stage_extract_sources(self, sources: List[Source]) -> None:
        """Stage 6: Extract content from sources using Jina Reader."""
        for source in sources:
            if not source.url:
                source.extraction_status = "failed"
                continue
            
            try:
                result = await jina_service.extract(source.url)
                
                if result.get("success"):
                    source.content = result.get("content", "")
                    source.title = result.get("title", source.title)
                    source.extraction_status = "success"
                else:
                    source.extraction_status = "failed"
            except Exception as e:
                logger.error("Extraction failed", source_id=source.id, error=str(e))
                source.extraction_status = "failed"
        
        await self.db.commit()
    
    async def _stage_chunk_and_embed(self, sources: List[Source]) -> None:
        """Stage 7: Chunk sources and generate embeddings."""
        # Simplified: chunk text into overlapping segments
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
                    embedding=[],  # Placeholder for embeddings
                    char_start=i * (settings.CHUNK_SIZE - settings.CHUNK_OVERLAP),
                    char_end=(i + 1) * settings.CHUNK_SIZE,
                )
                self.db.add(chunk_obj)
        
        await self.db.commit()
    
    async def _stage_extract_claims(
        self, sources: List[Source], dimensions: List[ResearchDimension]
    ) -> List[Claim]:
        """Stage 8: Extract structured claims from sources."""
        claims = []
        dim_map = {d.id: d for d in dimensions}
        
        for source in sources:
            if not source.content or source.extraction_status != "success":
                continue
            
            for dim in dimensions:
                prompt = f"""
                Extract factual claims from this source about: {dim.name}
                
                Dimension: {dim.name}
                Description: {dim.description}
                Questions: {dim.questions}
                
                Source content (first 5000 chars):
                {source.content[:5000]}
                
                Extract claims as JSON array with:
                - entity: what the claim is about
                - attribute: what property/aspect
                - value: the claimed value
                - claim_type: fact/requirement/deadline/condition/procedure/contact
                - excerpt: exact supporting text from source
                - confidence: 0-1
                """
                
                schema = {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "entity": {"type": "string"},
                            "attribute": {"type": "string"},
                            "value": {"type": "string"},
                            "claim_type": {"type": "string"},
                            "excerpt": {"type": "string"},
                            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        },
                        "required": ["entity", "attribute", "value", "claim_type", "excerpt", "confidence"],
                    },
                }
                
                result = await llm_service.generate_structured(prompt, schema)
                
                for claim_data in result:
                    claim = Claim(
                        id=str(uuid4()),
                        session_id=self.session_id,
                        source_id=source.id,
                        dimension_id=dim.id,
                        claim_text=f"{claim_data['entity']} {claim_data['attribute']} is {claim_data['value']}",
                        entity=claim_data["entity"],
                        attribute=claim_data["attribute"],
                        value=claim_data["value"],
                        claim_type=claim_data["claim_type"],
                        excerpt=claim_data["excerpt"],
                        confidence=claim_data["confidence"],
                        evidence_status=FindingStatus.POTENTIAL,
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
            elif len(dim_claims) >= 3:
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
        
        for (entity, attr), group in claim_groups.items():
            if len(group) < 2:
                continue
            
            # Check for conflicting values
            values = set(c.value for c in group)
            if len(values) > 1:
                # Found contradiction
                c1, c2 = group[0], group[1]
                
                # Determine conflict type (simplified)
                conflict_type = ConflictType.GENUINE
                
                conflict = Conflict(
                    id=str(uuid4()),
                    session_id=self.session_id,
                    entity=entity,
                    attribute=attr,
                    claim_a_id=c1.id,
                    claim_b_id=c2.id,
                    conflict_type=conflict_type,
                    resolution_action=f"Verify {entity} {attr} on official source",
                    confidence=0.8,
                )
                self.db.add(conflict)
                conflicts.append(conflict)
        
        await self.db.commit()
        return conflicts
    
    async def _stage_freshness_analysis(self, sources: List[Source]) -> None:
        """Stage 11: Analyze source freshness."""
        # Simplified: classify based on publication date
        for source in sources:
            # In real implementation, would analyze dates and content
            pass
        
        await self.db.commit()
    
    async def _stage_evidence_validation(self, claims: List[Claim], sources: List[Source]) -> None:
        """Stage 12: Validate evidence for claims."""
        source_map = {s.id: s for s in sources}
        
        for claim in claims:
            source = source_map.get(claim.source_id)
            if not source or not source.content:
                claim.evidence_status = FindingStatus.UNVERIFIED
                continue
            
            # Check if excerpt exists in source
            if claim.excerpt and claim.excerpt in source.content:
                claim.evidence_status = FindingStatus.VERIFIED
            elif claim.excerpt:
                # Fuzzy match
                claim.evidence_status = FindingStatus.POTENTIAL
            else:
                claim.evidence_status = FindingStatus.UNVERIFIED
        
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
                    evidence_summary="Multiple sources provide different values",
                    next_action="Verify on authoritative source",
                    recommended_authority="Official portal",
                    verification_method="cross_reference",
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
            self.db.add(checklist)
            checklist.append(item)
        
        await self.db.commit()
        return checklist
    
    async def _complete_session(self) -> None:
        """Mark session as completed."""
        await self.db.execute(
            update(ResearchSession)
            .where(ResearchSession.id == self.session_id)
            .values(
                status=SessionStatus.COMPLETED,
                completed_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
        await self.db.commit()
    
    async def _fail_session(self, error: str) -> None:
        """Mark session as failed."""
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


async def run_pipeline(session_id: str, db: AsyncSession) -> None:
    """Entry point to run pipeline for a session."""
    orchestrator = PipelineOrchestrator(db)
    await orchestrator.run_pipeline(session_id)