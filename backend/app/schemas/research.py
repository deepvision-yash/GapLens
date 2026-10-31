from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import Optional, List, Literal, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class SessionStatus(str, Enum):
    CREATED = "created"
    UNDERSTANDING = "understanding"
    SCOPE_REVIEW = "scope_review"
    READY = "ready"
    SEARCHING = "searching"
    EXTRACTING = "extracting"
    CLAIM_EXTRACTION = "claim_extraction"
    ANALYZING = "analyzing"
    GENERATING_CHECKLIST = "generating_checklist"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"


class FindingStatus(str, Enum):
    VERIFIED = "verified"
    POTENTIAL = "potential"
    UNCERTAIN = "uncertain"
    UNVERIFIED = "unverified"


class CoverageStatus(str, Enum):
    COVERED = "covered"
    PARTIAL = "partial"
    MISSING = "missing"
    CONFLICTING = "conflicting"
    OUTDATED = "outdated"
    WEAK_EVIDENCE = "weak_evidence"


class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ConflictType(str, Enum):
    GENUINE = "genuine"
    TEMPORAL = "temporal"
    CONTEXTUAL = "contextual"
    DEFINITIONAL = "definitional"
    JURISDICTIONAL = "jurisdictional"
    UNCERTAIN = "uncertain"


class SourceType(str, Enum):
    OFFICIAL_GOVERNMENT = "official_government"
    OFFICIAL_PORTAL = "official_portal"
    REGULATORY = "regulatory"
    ACADEMIC = "academic"
    NEWS = "news"
    POTENTIAL_OFFICIAL = "potential_official"
    GENERAL = "general"
    FORUM = "forum"
    COMMERCIAL = "commercial"
    UNKNOWN = "unknown"


class SourceInput(BaseModel):
    kind: Literal["url", "file"]
    url: Optional[HttpUrl] = None
    file_id: Optional[str] = None  # Reference to uploaded file


class ResearchGoal(BaseModel):
    original_query: str
    interpreted_objective: str
    entities: List[str] = []
    scope: List[str] = []
    geography: List[str] = []
    time_constraints: Optional[str] = None
    constraints: List[str] = []


class ResearchDimension(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    questions: List[str] = []
    coverage_status: CoverageStatus = CoverageStatus.MISSING
    claim_count: int = 0
    priority: int = 3  # 1-5


class ResearchSessionCreate(BaseModel):
    goal: str = Field(..., min_length=10, max_length=2000)
    sources: List[SourceInput] = []
    user_dimensions: Optional[List[ResearchDimension]] = None


class ResearchSessionResponse(BaseModel):
    id: str
    goal: str
    status: SessionStatus
    created_at: datetime
    updated_at: datetime
    source_count: int = 0
    dimension_count: int = 0
    is_partial: bool = False
    error: Optional[str] = None


class ResearchScopeResponse(BaseModel):
    session_id: str
    goal_understanding: ResearchGoal
    dimensions: List[ResearchDimension]
    status: SessionStatus


class DimensionUpdate(BaseModel):
    dimensions: List[ResearchDimension]


class SourceCreate(BaseModel):
    url: Optional[HttpUrl] = None
    file_id: Optional[str] = None


class SourceResponse(BaseModel):
    id: str
    session_id: str
    url: Optional[str] = None
    title: Optional[str] = None
    domain: Optional[str] = None
    source_type: SourceType = SourceType.UNKNOWN
    publication_date: Optional[datetime] = None
    last_modified: Optional[datetime] = None
    retrieval_date: datetime
    authority_score: float = 0.0
    relevance_score: float = 0.0
    extraction_status: Literal["pending", "success", "partial", "failed"] = "pending"
    content_preview: Optional[str] = None


class ClaimResponse(BaseModel):
    id: str
    session_id: str
    source_id: str
    dimension_id: str
    text: str
    entity: str
    attribute: str
    value: str
    claim_type: str
    excerpt: str
    confidence: float
    evidence_status: FindingStatus
    freshness: Optional[str] = None


class GapResponse(BaseModel):
    id: str
    session_id: str
    dimension_id: str
    title: str
    explanation: str
    priority: Priority
    evidence_summary: str
    next_action: str
    recommended_authority: Optional[str] = None
    verification_method: Literal["official_source", "cross_reference", "contact_authority", "calculate"] = "official_source"


class ConflictResponse(BaseModel):
    id: str
    session_id: str
    entity: str
    attribute: str
    claim_a: ClaimResponse
    claim_b: ClaimResponse
    conflict_type: ConflictType
    resolution_action: Optional[str] = None


class VerificationTaskResponse(BaseModel):
    id: str
    session_id: str
    dimension_id: str
    title: str
    priority: Priority
    explanation: str
    completed: bool = False
    recommended_authority: Optional[str] = None
    verification_method: Literal["official_source", "cross_reference", "contact_authority", "calculate"] = "official_source"
    source_ids: List[str] = []


class ChecklistUpdate(BaseModel):
    completed: bool


class SessionStatusResponse(BaseModel):
    session_id: str
    status: SessionStatus
    current_stage: str
    progress: int  # 0-100
    stages_completed: List[str] = []
    stages_pending: List[str] = []
    sources_found: int = 0
    claims_extracted: int = 0
    errors: List[str] = []
    is_partial: bool = False


class SSEEvent(BaseModel):
    event: str
    data: Dict[str, Any]
    session_id: str


class ResearchResultsResponse(BaseModel):
    session_id: str
    goal: ResearchGoal
    dimensions: List[ResearchDimension]
    sources: List[SourceResponse]
    claims: List[ClaimResponse]
    gaps: List[GapResponse]
    conflicts: List[ConflictResponse]
    checklist: List[VerificationTaskResponse]
    status: SessionStatus
    completed_at: Optional[datetime] = None
    is_partial: bool = False