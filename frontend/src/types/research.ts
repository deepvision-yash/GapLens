export type SessionStatus =
  | 'created'
  | 'understanding'
  | 'scope_review'
  | 'ready'
  | 'searching'
  | 'extracting'
  | 'claim_extraction'
  | 'analyzing'
  | 'generating_checklist'
  | 'completed'
  | 'partial'
  | 'failed'

export type FindingStatus = 'verified' | 'potential' | 'uncertain' | 'unverified'

export type CoverageStatus =
  | 'covered'
  | 'partial'
  | 'missing'
  | 'conflicting'
  | 'outdated'
  | 'weak_evidence'

export type FreshnessStatus =
  | 'current'
  | 'aging'
  | 'outdated'
  | 'expired'
  | 'undated'
  | 'future'

export type Priority = 'critical' | 'high' | 'medium' | 'low'

export interface ResearchSession {
  id: string
  title: string
  goal: string
  status: SessionStatus
  createdAt: string
  updatedAt: string
  isPartial?: boolean
  sourceCount?: number
  dimensionCount?: number
  claimCount?: number
  gapCount?: number
  conflictCount?: number
}

export interface ResearchDimension {
  id: string
  name: string
  description: string
  coverageStatus?: CoverageStatus
  claimCount?: number
}

export interface ResearchSource {
  id: string
  title: string
  url?: string
  domain?: string
  sourceType: string
  publicationDate?: string
  lastModified?: string
  retrievalDate?: string
  extractionStatus?: 'pending' | 'success' | 'partial' | 'failed'
}

export interface EvidenceClaim {
  id: string
  text: string
  status: FindingStatus
  dimensionId?: string
  sourceId?: string
  exactExcerpt?: string
  confidence?: number
  freshness?: FreshnessStatus
}

export interface ResearchGap {
  id: string
  title: string
  explanation: string
  priority: Priority
  dimensionId?: string
  relatedClaimIds: string[]
  nextAction?: string
}

export interface ResearchConflict {
  id: string
  title: string
  claimA: EvidenceClaim
  claimB: EvidenceClaim
  conflictType: 'genuine' | 'temporal' | 'contextual' | 'definitional' | 'jurisdictional' | 'uncertain'
  resolutionAction?: string
}

export interface VerificationTask {
  id: string
  title: string
  priority: Priority
  explanation: string
  completed: boolean
  dimensionId?: string
  sourceIds: string[]
  recommendedAuthority?: string
  verificationMethod?: string
}

export interface SourceInput {
  kind: 'url' | 'file'
  url?: string
  file?: File
}

export const STATUS_LABELS: Record<SessionStatus, string> = {
  created: 'Created',
  understanding: 'Understanding goal',
  scope_review: 'Scope review',
  ready: 'Ready',
  searching: 'Searching sources',
  extracting: 'Extracting content',
  claim_extraction: 'Extracting claims',
  analyzing: 'Analyzing evidence',
  generating_checklist: 'Generating checklist',
  completed: 'Completed',
  partial: 'Partial',
  failed: 'Failed',
}

export const COVERAGE_STATUS_LABELS: Record<CoverageStatus, string> = {
  covered: 'Covered',
  partial: 'Partial',
  missing: 'Missing',
  conflicting: 'Conflicting',
  outdated: 'Outdated',
  weak_evidence: 'Weak evidence',
}

export const FINDING_STATUS_LABELS: Record<FindingStatus, string> = {
  verified: 'Verified',
  potential: 'Potential',
  uncertain: 'Uncertain',
  unverified: 'Unverified',
}

export const PRIORITY_LABELS: Record<Priority, string> = {
  critical: 'Critical',
  high: 'High',
  medium: 'Medium',
  low: 'Low',
}

export const FRESHNESS_LABELS: Record<FreshnessStatus, string> = {
  current: 'Current',
  aging: 'Aging',
  outdated: 'Outdated',
  expired: 'Expired',
  undated: 'Undated',
  future: 'Future-dated',
}