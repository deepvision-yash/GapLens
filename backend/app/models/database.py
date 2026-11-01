from sqlalchemy import (
    Column, String, Text, DateTime, Float, Integer, Boolean, ForeignKey,
    Enum as SQLEnum, JSON, Index, text
)
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from uuid import uuid4
import enum

from app.schemas.research import (
    SessionStatus, FindingStatus, CoverageStatus, Priority,
    ConflictType, SourceType
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(SQLUUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(320), unique=True, index=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    research_sessions = relationship("ResearchSession", back_populates="owner")


class ResearchSession(Base):
    __tablename__ = "research_sessions"
    
    id = Column(SQLUUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    goal_text = Column(Text, nullable=False)
    goal_json = Column(JSON, nullable=False)  # ResearchGoal
    dimensions_json = Column(JSON, nullable=False)  # ResearchDimension[]
    status = Column(SQLEnum(SessionStatus), default=SessionStatus.CREATED, nullable=False)
    is_partial = Column(Boolean, default=False)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    owner_id = Column(SQLUUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    owner = relationship("User", back_populates="research_sessions")
    
    # Relationships
    sources = relationship("Source", back_populates="session", cascade="all, delete-orphan")
    claims = relationship("Claim", back_populates="session", cascade="all, delete-orphan")
    gaps = relationship("Gap", back_populates="session", cascade="all, delete-orphan")
    conflicts = relationship("Conflict", back_populates="session", cascade="all, delete-orphan")
    checklist_items = relationship("ChecklistItem", back_populates="session", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("ix_sessions_status", "status"),
        Index("ix_sessions_created", "created_at"),
    )


class Source(Base):
    __tablename__ = "sources"
    
    id = Column(SQLUUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    session_id = Column(SQLUUID(as_uuid=False), ForeignKey("research_sessions.id", ondelete="CASCADE"), nullable=False)
    url = Column(Text, nullable=True)
    title = Column(Text, nullable=True)
    domain = Column(String(255), nullable=True)
    source_type = Column(SQLEnum(SourceType), default=SourceType.UNKNOWN, nullable=False)
    publication_date = Column(DateTime, nullable=True)
    last_modified = Column(DateTime, nullable=True)
    retrieval_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    authority_score = Column(Float, default=0.0)
    relevance_score = Column(Float, default=0.0)
    extraction_status = Column(String(20), default="pending")  # pending, success, partial, failed
    content = Column(Text, nullable=True)  # Full markdown content
    metadata_json = Column(JSON, nullable=True)  # Raw extraction metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    session = relationship("ResearchSession", back_populates="sources")
    chunks = relationship("SourceChunk", back_populates="source", cascade="all, delete-orphan")
    claims = relationship("Claim", back_populates="source", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("ix_sources_session", "session_id"),
        Index("ix_sources_url", "url"),
    )


class SourceChunk(Base):
    __tablename__ = "source_chunks"
    
    id = Column(SQLUUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    source_id = Column(SQLUUID(as_uuid=False), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    token_count = Column(Integer, nullable=False)
    embedding = Column(JSON, nullable=True)  # Store as JSON array for sqlite-vec compatibility
    char_start = Column(Integer, nullable=False)
    char_end = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    source = relationship("Source", back_populates="chunks")
    
    __table_args__ = (
        Index("ix_chunks_source", "source_id"),
    )


class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(SQLUUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    session_id = Column(SQLUUID(as_uuid=False), ForeignKey("research_sessions.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(SQLUUID(as_uuid=False), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    dimension_id = Column(String(100), nullable=False)
    claim_text = Column(Text, nullable=False)
    entity = Column(String(255), nullable=False)
    attribute = Column(String(255), nullable=False)
    value = Column(Text, nullable=False)
    claim_type = Column(String(50), nullable=False)
    excerpt = Column(Text, nullable=False)
    date_context = Column(JSON, nullable=True)
    confidence = Column(Float, default=0.0)
    evidence_status = Column(SQLEnum(FindingStatus), default=FindingStatus.UNVERIFIED, nullable=False)
    freshness = Column(String(30), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    session = relationship("ResearchSession", back_populates="claims")
    source = relationship("Source", back_populates="claims")
    
    __table_args__ = (
        Index("ix_claims_session", "session_id"),
        Index("ix_claims_dimension", "dimension_id"),
        Index("ix_claims_entity_attr", "entity", "attribute"),
    )


class Gap(Base):
    __tablename__ = "gaps"
    
    id = Column(SQLUUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    session_id = Column(SQLUUID(as_uuid=False), ForeignKey("research_sessions.id", ondelete="CASCADE"), nullable=False)
    dimension_id = Column(String(100), nullable=False)
    title = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    priority = Column(SQLEnum(Priority), nullable=False)
    evidence_summary = Column(Text, nullable=False)
    next_action = Column(Text, nullable=False)
    recommended_authority = Column(Text, nullable=True)
    verification_method = Column(String(30), default="official_source")
    claim_ids = Column(JSON, nullable=True)  # List of claim IDs
    source_ids = Column(JSON, nullable=True)  # List of source IDs
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    session = relationship("ResearchSession", back_populates="gaps")
    
    __table_args__ = (
        Index("ix_gaps_session", "session_id"),
        Index("ix_gaps_priority", "priority"),
    )


class Conflict(Base):
    __tablename__ = "conflicts"
    
    id = Column(SQLUUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    session_id = Column(SQLUUID(as_uuid=False), ForeignKey("research_sessions.id", ondelete="CASCADE"), nullable=False)
    entity = Column(String(255), nullable=False)
    attribute = Column(String(255), nullable=False)
    claim_a_id = Column(SQLUUID(as_uuid=False), ForeignKey("claims.id"), nullable=False)
    claim_b_id = Column(SQLUUID(as_uuid=False), ForeignKey("claims.id"), nullable=False)
    conflict_type = Column(SQLEnum(ConflictType), nullable=False)
    resolution_action = Column(Text, nullable=True)
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    session = relationship("ResearchSession", back_populates="conflicts")
    claim_a = relationship("Claim", foreign_keys=[claim_a_id])
    claim_b = relationship("Claim", foreign_keys=[claim_b_id])
    
    __table_args__ = (
        Index("ix_conflicts_session", "session_id"),
    )


class ChecklistItem(Base):
    __tablename__ = "checklist_items"
    
    id = Column(SQLUUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    session_id = Column(SQLUUID(as_uuid=False), ForeignKey("research_sessions.id", ondelete="CASCADE"), nullable=False)
    dimension_id = Column(String(100), nullable=False)
    title = Column(Text, nullable=False)
    priority = Column(SQLEnum(Priority), nullable=False)
    explanation = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)
    recommended_authority = Column(Text, nullable=True)
    verification_method = Column(String(30), default="official_source")
    source_ids = Column(JSON, nullable=True)  # List of source IDs
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    session = relationship("ResearchSession", back_populates="checklist_items")
    
    __table_args__ = (
        Index("ix_checklist_session", "session_id"),
        Index("ix_checklist_completed", "completed"),
    )
