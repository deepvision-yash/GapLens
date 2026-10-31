import { ResearchSession, ResearchResultsResponse, SessionStatus, ResearchDimension, CoverageStatus, SourceResponse, ClaimResponse, GapResponse, ConflictResponse, VerificationTaskResponse, Priority, FindingStatus } from '@/types/research';

// Mock data for demo mode
const MOCK_SESSIONS: ResearchSession[] = [
  {
    id: 'demo-1',
    title: 'Central Sector Scholarship 2026 Verification',
    goal: 'What should I verify before applying for Central Sector Scholarship 2026?',
    status: 'completed' as SessionStatus,
    createdAt: new Date(Date.now() - 2 * 3600000).toISOString(),
    updatedAt: new Date(Date.now() - 1 * 3600000).toISOString(),
    sourceCount: 12,
    dimensionCount: 8,
    isPartial: false,
  },
  {
    id: 'demo-2',
    title: 'RBI Account Aggregator License Requirements',
    goal: 'RBI Account Aggregator License Requirements',
    status: 'partial' as SessionStatus,
    createdAt: new Date(Date.now() - 24 * 3600000).toISOString(),
    updatedAt: new Date(Date.now() - 23 * 3600000).toISOString(),
    sourceCount: 8,
    dimensionCount: 6,
    isPartial: true,
  },
];

const MOCK_DIMENSIONS: ResearchDimension[] = [
  { id: 'dim-1', name: 'Eligibility Criteria', description: 'Who can apply, income limits, categories', coverageStatus: 'covered' as CoverageStatus, claimCount: 5, priority: 5 },
  { id: 'dim-2', name: 'Application Deadline', description: 'Last date to apply, cycle dates', coverageStatus: 'conflicting' as CoverageStatus, claimCount: 3, priority: 5 },
  { id: 'dim-3', name: 'Required Documents', description: 'List of documents needed for application', coverageStatus: 'covered' as CoverageStatus, claimCount: 4, priority: 4 },
  { id: 'dim-4', name: 'Financial Benefits', description: 'Scholarship amount, disbursement schedule', coverageStatus: 'covered' as CoverageStatus, claimCount: 2, priority: 3 },
  { id: 'dim-5', name: 'Renewal Conditions', description: 'CGPA requirements, renewal process', coverageStatus: 'missing' as CoverageStatus, claimCount: 0, priority: 5 },
  { id: 'dim-6', name: 'Official Application Process', description: 'Step-by-step application procedure', coverageStatus: 'partial' as CoverageStatus, claimCount: 2, priority: 3 },
  { id: 'dim-7', name: 'Contact Information', description: 'Helpline, email, office address', coverageStatus: 'covered' as CoverageStatus, claimCount: 1, priority: 2 },
  { id: 'dim-8', name: 'Reservation Policies', description: 'Category-wise reservations, quotas', coverageStatus: 'weak_evidence' as CoverageStatus, claimCount: 1, priority: 2 },
];

const MOCK_SOURCES: SourceResponse[] = [
  { id: 'src-1', url: 'https://scholarships.gov.in/central-sector-scheme', title: 'Central Sector Scholarship - Official Portal', domain: 'scholarships.gov.in', sourceType: 'official_portal', publicationDate: '2024-01-15T00:00:00Z', lastModified: '2024-06-01T00:00:00Z', retrievalDate: new Date().toISOString(), authorityScore: 0.95, relevanceScore: 0.98, extractionStatus: 'success', contentPreview: 'Central Sector Scholarship Scheme for College and University Students...' },
  { id: 'src-2', url: 'https://www.nsp.gov.in/', title: 'National Scholarship Portal', domain: 'nsp.gov.in', sourceType: 'official_portal', publicationDate: '2024-02-01T00:00:00Z', lastModified: '2024-07-15T00:00:00Z', retrievalDate: new Date().toISOString(), authorityScore: 0.9, relevanceScore: 0.95, extractionStatus: 'success', contentPreview: 'National Scholarship Portal - Central Sector Scheme guidelines...' },
  { id: 'src-3', url: 'https://pib.gov.in/PressReleasePage.aspx?PRID=1987654', title: 'PIB Release: Central Sector Scholarship 2024-25', domain: 'pib.gov.in', sourceType: 'official_government', publicationDate: '2024-07-01T00:00:00Z', retrievalDate: new Date().toISOString(), authorityScore: 0.92, relevanceScore: 0.88, extractionStatus: 'success', contentPreview: 'Ministry of Education announces Central Sector Scholarship for 2024-25 academic year...' },
  { id: 'src-4', url: 'https://www.ugc.gov.in/pdfnews/4054544_Central-Sector-Scholarship.pdf', title: 'UGC Guidelines for Central Sector Scholarship', domain: 'ugc.gov.in', sourceType: 'official_government', publicationDate: '2023-12-20T00:00:00Z', retrievalDate: new Date().toISOString(), authorityScore: 0.85, relevanceScore: 0.82, extractionStatus: 'success', contentPreview: 'University Grants Commission guidelines for implementation of Central Sector Scheme...' },
  { id: 'src-5', url: 'https://www.careers360.com/scholarships/central-sector-scholarship', title: 'Central Sector Scholarship - Complete Guide', domain: 'careers360.com', sourceType: 'general', publicationDate: '2024-03-10T00:00:00Z', retrievalDate: new Date().toISOString(), authorityScore: 0.4, relevanceScore: 0.75, extractionStatus: 'success', contentPreview: 'Complete guide to Central Sector Scholarship eligibility, application process...' },
];

const MOCK_CLAIMS: ClaimResponse[] = [
  { id: 'cl-1', sourceId: 'src-1', dimensionId: 'dim-1', text: 'Family income must not exceed ₹8 lakh per annum', status: 'verified' as FindingStatus, exactExcerpt: 'The annual family income of the applicant should not exceed Rs. 8 lakh per annum', confidence: 0.95, freshness: 'current' },
  { id: 'cl-2', sourceId: 'src-2', dimensionId: 'dim-1', text: 'Income certificate must be issued by competent authority', status: 'verified' as FindingStatus, exactExcerpt: 'Income certificate issued by Tehsildar or above rank officer is mandatory', confidence: 0.9, freshness: 'current' },
  { id: 'cl-3', sourceId: 'src-1', dimensionId: 'dim-2', text: 'Application deadline is 31 October 2025', status: 'verified' as FindingStatus, exactExcerpt: 'Last date for submission of online application is 31st October 2025', confidence: 0.9, freshness: 'current' },
  { id: 'cl-4', sourceId: 'src-5', dimensionId: 'dim-2', text: 'Application deadline is 15 November 2025', status: 'potential' as FindingStatus, exactExcerpt: 'Students can apply until 15th November 2025 for the current cycle', confidence: 0.7, freshness: 'aging' },
  { id: 'cl-5', sourceId: 'src-1', dimensionId: 'dim-3', text: 'Required documents: Aadhaar, Income Certificate, Caste Certificate, Bank Passbook', status: 'verified' as FindingStatus, exactExcerpt: 'Documents required: Aadhaar card, Income certificate, Caste certificate (if applicable), Bank passbook copy', confidence: 0.95, freshness: 'current' },
  { id: 'cl-6', sourceId: 'src-2', dimensionId: 'dim-3', text: 'Additional document: Bonafide certificate from institution', status: 'potential' as FindingStatus, exactExcerpt: 'Bonafide certificate from current institution is also required', confidence: 0.8, freshness: 'current' },
  { id: 'cl-7', sourceId: 'src-3', dimensionId: 'dim-4', text: 'Scholarship amount: ₹10,000 per annum for graduation, ₹20,000 for post-graduation', status: 'verified' as FindingStatus, exactExcerpt: 'Scholarship of Rs. 10,000 per annum for graduation courses and Rs. 20,000 per annum for post-graduation courses', confidence: 0.9, freshness: 'current' },
  { id: 'cl-8', sourceId: 'src-4', dimensionId: 'dim-6', text: 'Apply online through NSP portal', status: 'verified' as FindingStatus, exactExcerpt: 'Applications must be submitted online through the National Scholarship Portal (NSP)', confidence: 0.95, freshness: 'current' },
  { id: 'cl-9', sourceId: 'src-1', dimensionId: 'dim-7', text: 'Helpline: 011-23381212, Email: helpdesk@nsp.gov.in', status: 'verified' as FindingStatus, exactExcerpt: 'For queries contact helpdesk at 011-23381212 or email helpdesk@nsp.gov.in', confidence: 0.9, freshness: 'current' },
];

const MOCK_GAPS: GapResponse[] = [
  { id: 'gap-1', dimensionId: 'dim-5', title: 'Missing: Renewal Conditions', explanation: 'No sources found covering renewal conditions, CGPA requirements, or renewal application process for subsequent years', priority: 'critical' as Priority, relatedClaimIds: [], nextAction: 'Check NSP portal for renewal guidelines; contact helpdesk', recommendedAuthority: 'National Scholarship Portal (nsp.gov.in)', verificationMethod: 'official_source' },
  { id: 'gap-2', dimensionId: 'dim-2', title: 'Conflict: Application Deadline', explanation: 'Two sources provide different deadlines: Official portal states 31 Oct 2025, secondary source states 15 Nov 2025', priority: 'critical' as Priority, relatedClaimIds: ['cl-3', 'cl-4'], nextAction: 'Verify deadline on NSP portal; check latest PIB release', recommendedAuthority: 'National Scholarship Portal', verificationMethod: 'cross_reference' },
  { id: 'gap-3', dimensionId: 'dim-3', title: 'Partial: Document Requirements', explanation: 'Official portal lists 4 required documents; secondary source mentions additional bonafide certificate', priority: 'high' as Priority, relatedClaimIds: ['cl-5', 'cl-6'], nextAction: 'Verify with college nodal officer if bonafide certificate is mandatory', recommendedAuthority: 'College Nodal Officer / NSP Portal', verificationMethod: 'official_source' },
  { id: 'gap-4', dimensionId: 'dim-8', title: 'Weak Evidence: Reservation Policies', explanation: 'Only one source mentions reservation categories; no official notification found', priority: 'medium' as Priority, relatedClaimIds: ['cl-7'], nextAction: 'Check official notification for category-wise quota details', recommendedAuthority: 'Ministry of Education Notification', verificationMethod: 'official_source' },
];

const MOCK_CONFLICTS: ConflictResponse[] = [
  { id: 'conf-1', title: 'Application Deadline Conflict', entity: 'application deadline', attribute: 'date', claimA: MOCK_CLAIMS[2], claimB: MOCK_CLAIMS[3], conflictType: 'genuine', resolutionAction: 'Official portal (scholarships.gov.in) is authoritative; secondary source may be outdated', confidence: 0.9 },
];

const MOCK_CHECKLIST: VerificationTaskResponse[] = [
  { id: 'task-1', dimensionId: 'dim-5', title: 'Find renewal conditions on NSP portal', priority: 'critical' as Priority, explanation: 'No sources found for renewal conditions; critical for multi-year scholarship', completed: false, recommendedAuthority: 'National Scholarship Portal (nsp.gov.in)', verificationMethod: 'official_source', sourceIds: [] },
  { id: 'task-2', dimensionId: 'dim-2', title: 'Confirm application deadline on NSP portal', priority: 'critical' as Priority, explanation: 'Conflicting deadlines: 31 Oct vs 15 Nov; must verify official date', completed: false, recommendedAuthority: 'National Scholarship Portal (scholarships.gov.in)', verificationMethod: 'cross_reference', sourceIds: ['src-1', 'src-5'] },
  { id: 'task-3', dimensionId: 'dim-3', title: 'Verify complete document list with college nodal officer', priority: 'high' as Priority, explanation: 'Official portal lists 4 docs; secondary source adds bonafide certificate', completed: false, recommendedAuthority: 'College Nodal Officer', verificationMethod: 'official_source', sourceIds: ['src-1', 'src-2'] },
  { id: 'task-4', dimensionId: 'dim-8', title: 'Check official notification for reservation quotas', priority: 'medium' as Priority, explanation: 'Only weak evidence for reservation policies from secondary source', completed: false, recommendedAuthority: 'Ministry of Education Official Notification', verificationMethod: 'official_source', sourceIds: [] },
];

// Simulated delay for realistic API feel
const DELAY = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export class MockApiService {
  private static instance: MockApiService;
  private sessions: Map<string, any> = new Map();
  private sessionCounter = 0;

  static getInstance(): MockApiService {
    if (!MockApiService.instance) {
      MockApiService.instance = new MockApiService();
    }
    return MockApiService.instance;
  }

  async createResearch(payload: { goal: string; sources?: any[] }): Promise<{ id: string; status: string }> {
    await DELAY(500);
    this.sessionCounter++;
    const sessionId = `demo-${Date.now()}-${this.sessionCounter}`;
    this.sessions.set(sessionId, {
      id: sessionId,
      goal: payload.goal,
      sources: payload.sources || [],
      status: 'created',
      createdAt: new Date().toISOString(),
    });
    return { id: sessionId, status: 'created' };
  }

  async understandGoal(sessionId: string) {
    await DELAY(1000);
    return {
      sessionId,
      goalUnderstanding: {
        originalQuery: 'What should I verify before applying for Central Sector Scholarship 2026?',
        interpretedObjective: 'Verify all eligibility criteria, deadlines, documents, and renewal conditions for Central Sector Scholarship 2026',
        entities: ['Central Sector Scholarship', '2026'],
        scope: ['eligibility', 'deadlines', 'documents', 'benefits', 'renewal', 'process', 'contact'],
        geography: ['India'],
        timeConstraints: '2025-26 academic cycle',
        constraints: ['income < 8L', 'first-year student'],
      },
      dimensions: MOCK_DIMENSIONS,
      status: 'scope_review' as const,
    };
  }

  async getScope(sessionId: string) {
    await DELAY(300);
    return {
      sessionId,
      goalUnderstanding: {
        originalQuery: 'What should I verify before applying for Central Sector Scholarship 2026?',
        interpretedObjective: 'Verify all eligibility criteria, deadlines, documents, and renewal conditions for Central Sector Scholarship 2026',
        entities: ['Central Sector Scholarship', '2026'],
        scope: ['eligibility', 'deadlines', 'documents', 'benefits', 'renewal', 'process', 'contact'],
        geography: ['India'],
        timeConstraints: '2025-26 academic cycle',
        constraints: ['income < 8L', 'first-year student'],
      },
      dimensions: MOCK_DIMENSIONS,
      status: 'scope_review' as const,
    };
  }

  async updateScope(sessionId: string, dimensions: any[]) {
    await DELAY(300);
    return { sessionId, dimensions, status: 'scope_review' };
  }

  async startResearch(sessionId: string) {
    await DELAY(300);
    // Simulate pipeline progression
    this.sessions.set(sessionId, { ...this.sessions.get(sessionId), status: 'running' });
    return { message: 'Research started', sessionId };
  }

  async getStatus(sessionId: string): Promise<{
  sessionId: string;
  status: SessionStatus;
  currentStage: string;
  progress: number;
  stagesCompleted: string[];
  stagesPending: string[];
  sourcesFound: number;
  claimsExtracted: number;
  errors: string[];
  isPartial: boolean;
}> {
    await DELAY(200);
    const session = this.sessions.get(sessionId) || { status: 'completed' };
    const status = session.status || 'completed';
    
    const progressMap: Record<string, number> = {
      created: 0,
      understanding: 5,
      scope_review: 15,
      ready: 20,
      searching: 30,
      extracting: 45,
      claim_extraction: 60,
      analyzing: 70,
      generating_checklist: 90,
      completed: 100,
      partial: 100,
      failed: 0,
    };

    const stages = [
      'understanding', 'dimensions', 'scope_review', 'query_planning',
      'searching', 'extracting', 'chunking', 'claims',
      'coverage', 'contradictions', 'freshness', 'evidence',
      'gaps', 'checklist',
    ];

    const completedIdx = stages.indexOf('scope_review');
    
    return {
      sessionId,
      status: status as SessionStatus,
      currentStage: status,
      progress: progressMap[status] || 0,
      stagesCompleted: stages.slice(0, Math.max(0, completedIdx + 1)),
      stagesPending: stages.slice(Math.max(0, completedIdx + 1)),
      sourcesFound: MOCK_SOURCES.length,
      claimsExtracted: MOCK_CLAIMS.length,
      errors: [],
      isPartial: false,
    };
  }

  async getResults(sessionId: string): Promise<ResearchResultsResponse> {
    await DELAY(500);
    return {
      sessionId,
      goal: {
        originalQuery: 'What should I verify before applying for Central Sector Scholarship 2026?',
        interpretedObjective: 'Verify all eligibility criteria, deadlines, documents, and renewal conditions for Central Sector Scholarship 2026',
        entities: [{ name: 'Central Sector Scholarship', type: 'scholarship' }, { name: '2026', type: 'year' }],
        scope: ['eligibility', 'deadlines', 'documents', 'benefits', 'renewal', 'process', 'contact'],
        geography: ['India'],
        timeConstraints: '2025-26 academic cycle',
        constraints: ['income < 8L', 'first-year student'],
      },
      dimensions: MOCK_DIMENSIONS,
      sources: MOCK_SOURCES,
      claims: MOCK_CLAIMS,
      gaps: MOCK_GAPS,
      conflicts: MOCK_CONFLICTS,
      checklist: MOCK_CHECKLIST,
      status: 'completed' as const,
      completedAt: new Date().toISOString(),
      isPartial: false,
    };
  }

  async getSources(sessionId: string) {
    await DELAY(200);
    return MOCK_SOURCES;
  }

  async getClaims(sessionId: string) {
    await DELAY(200);
    return MOCK_CLAIMS;
  }

  async getGaps(sessionId: string) {
    await DELAY(200);
    return MOCK_GAPS;
  }

  async getConflicts(sessionId: string) {
    await DELAY(200);
    return MOCK_CONFLICTS;
  }

  async getChecklist(sessionId: string) {
    await DELAY(200);
    return MOCK_CHECKLIST;
  }

  async updateChecklistTask(sessionId: string, taskId: string, completed: boolean) {
    await DELAY(200);
    const task = MOCK_CHECKLIST.find(t => t.id === taskId);
    if (task) {
      return { ...task, completed };
    }
    throw new Error('Task not found');
  }

  async *streamEvents(sessionId: string) {
    // Simulate SSE events for progress
    const stages = [
      { stage: 'understanding', progress: 5, message: 'Understanding research goal...' },
      { stage: 'dimensions', progress: 10, message: 'Generating research dimensions...' },
      { stage: 'scope_review', progress: 15, message: 'Awaiting scope confirmation...' },
      { stage: 'searching', progress: 30, message: 'Searching for sources...' },
      { stage: 'extracting', progress: 45, message: 'Extracting source content...' },
      { stage: 'claims', progress: 60, message: 'Extracting claims...' },
      { stage: 'coverage', progress: 70, message: 'Analyzing coverage...' },
      { stage: 'contradictions', progress: 75, message: 'Detecting contradictions...' },
      { stage: 'freshness', progress: 80, message: 'Analyzing freshness...' },
      { stage: 'evidence', progress: 85, message: 'Validating evidence...' },
      { stage: 'gaps', progress: 90, message: 'Prioritizing gaps...' },
      { stage: 'checklist', progress: 95, message: 'Generating checklist...' },
      { stage: 'completed', progress: 100, message: 'Research completed!' },
    ];

    for (const stage of stages) {
      yield { event: 'progress', data: JSON.stringify({ sessionId, ...stage }) };
      await DELAY(800);
    }
  }
}

// Export singleton
export const mockApi = MockApiService.getInstance();

// Helper to check if we're in demo mode
export function isDemoMode(): boolean {
  return process.env.NEXT_PUBLIC_DEMO_MODE === 'true' || typeof window !== 'undefined' && localStorage.getItem('demoMode') === 'true';
}