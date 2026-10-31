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

export type ConflictType =
  | 'genuine'
  | 'temporal'
  | 'contextual'
  | 'definitional'
  | 'jurisdictional'
  | 'uncertain'

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
  priority?: number
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
  authorityScore?: number
  relevanceScore?: number
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
  conflictType: ConflictType
  resolutionAction?: string
  confidence: number
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

export interface SourceResponse {
  id: string
  title: string
  url?: string
  domain?: string
  sourceType: string
  publicationDate?: string
  lastModified?: string
  retrievalDate?: string
  authorityScore: number
  relevanceScore: number
  extractionStatus: string
  contentPreview?: string
}

export interface ClaimResponse {
  id: string
  text: string
  status: string
  dimensionId?: string
  sourceId?: string
  exactExcerpt?: string
  confidence?: number
  freshness?: string
}

export interface GapResponse {
  id: string
  title: string
  explanation: string
  priority: Priority
  dimensionId?: string
  relatedClaimIds: string[]
  nextAction?: string
  recommendedAuthority?: string
  verificationMethod?: string
}

export interface ConflictResponse {
  id: string
  title: string
  claimA: ClaimResponse
  claimB: ClaimResponse
  conflictType: ConflictType
  resolutionAction?: string
  confidence: number
  entity?: string
  attribute?: string
}

export interface VerificationTaskResponse {
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

export interface ResearchResultsResponse {
  sessionId: string
  goal: {
    originalQuery: string
    interpretedObjective: string
    entities: Array<{ name: string; type: string }>
    scope: string[]
    geography: string[]
    timeConstraints: string | null
    constraints: string[]
  }
  dimensions: Array<{
    id: string
    name: string
    description: string
    coverageStatus?: CoverageStatus
    claimCount?: number
  }>
  sources: SourceResponse[]
  claims: ClaimResponse[]
  gaps: GapResponse[]
  conflicts: ConflictResponse[]
  checklist: VerificationTaskResponse[]
  status: 'completed' | 'partial' | 'failed'
  completedAt?: string
  isPartial: boolean
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

export const COVERAGE_STATUS_LABELS: Record<string, string> = {
  covered: 'Covered',
  partial: 'Partial',
  missing: 'Missing',
  conflicting: 'Conflicting',
  outdated: 'Outdated',
  weak_evidence: 'Weak evidence',
}

export const FINDING_STATUS_LABELS: Record<string, string> = {
  verified: 'Verified',
  potential: 'Potential',
  uncertain: 'Uncertain',
  unverified: 'Unverified',
}

export const PRIORITY_LABELS: Record<string, string> = {
  critical: 'Critical',
  high: 'High',
  medium: 'Medium',
  low: 'Low',
}

export const FRESHNESS_LABELS: Record<string, string> = {
  current: 'Current',
  aging: 'Aging',
  outdated: 'Outdated',
  expired: 'Expired',
  undated: 'Undated',
  future: 'Future-dated',
}