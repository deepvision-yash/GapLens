'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { mockApi, isDemoMode } from '@/services/mockApi'
import { ResearchResultsResponse, SessionStatus, ResearchDimension, CoverageStatus, SourceResponse, ClaimResponse, GapResponse, ConflictResponse, VerificationTaskResponse, Priority, FindingStatus } from '@/types/research'
import { formatRelativeTime } from '@/lib/utils'
import { ArrowRight, ArrowLeft, AlertCircle, CheckCircle, Info, AlertTriangle, Clock, FileText, Link, Check, X, ChevronRight, Download, RefreshCw } from 'lucide-react'

export default function ResearchWorkspacePage() {
  const router = useRouter()
  const params = useParams()
  const sessionId = params.id as string

  const [results, setResults] = useState<ResearchResultsResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'overview' | 'coverage' | 'gaps' | 'conflicts' | 'sources' | 'verification'>('overview')
  const [selectedClaim, setSelectedClaim] = useState<any>(null)
  const [showEvidenceDrawer, setShowEvidenceDrawer] = useState(false)

  useEffect(() => {
    const loadResults = async () => {
      setLoading(true)
      setError(null)
      try {
        let data: any
        if (isDemoMode()) {
          data = await mockApi.getResults(sessionId || 'demo-1')
        } else {
          const response = await fetch(`/api/research/${sessionId}/results`)
          if (!response.ok) throw new Error('Failed to load results')
          data = await response.json()
        }
        setResults(data)
      } catch (err) {
        console.error('Failed to load results:', err)
        setError('Failed to load research results')
      } finally {
        setLoading(false)
      }
    }

    if (sessionId) {
      loadResults()
    } else {
      router.push('/research/new')
    }
  }, [sessionId, router])

  if (!sessionId) {
    return null
  }

  if (loading) {
    return (
      <div className="w-full flex flex-col items-center justify-center px-4 py-8 md:py-12 select-none min-h-screen bg-background">
        <div className="w-full max-w-[760px] text-center">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded bg-surface-container-high border border-outline-variant mb-4">
            <span className="w-1.5 h-1.5 rounded-full bg-primary-container"></span>
            <span className="font-data-sm text-data-sm text-on-surface-variant uppercase tracking-wider">GapLens Core v1.4</span>
          </div>
          <div className="flex flex-col items-center gap-4">
            <div className="animate-spin rounded-full h-10 w-10 border-3 border-primary-container border-t-transparent"></div>
            <p className="font-body-md text-body-md text-on-surface-variant">Loading research results...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="w-full flex flex-col items-center justify-center px-4 py-8 md:py-12 select-none min-h-screen bg-background">
        <div className="w-full max-w-[760px] text-center">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded bg-surface-container-high border border-outline-variant mb-4">
            <span className="w-1.5 h-1.5 rounded-full bg-primary-container"></span>
            <span className="font-data-sm text-data-sm text-on-surface-variant uppercase tracking-wider">GapLens Core v1.4</span>
          </div>
          <div className="flex flex-col items-center gap-4">
            <AlertCircle className="h-12 w-12 text-error" />
            <h2 className="font-headline-sm text-headline-sm text-on-surface">Failed to load results</h2>
            <p className="font-body-md text-body-md text-on-surface-variant max-w-[580px] mx-auto text-center">{error}</p>
            <button onClick={() => router.push('/research/new')} className="mt-4 px-6 py-2.5 rounded-lg font-label-md text-label-md font-medium transition-all duration-150 flex items-center justify-center gap-2 bg-primary-container text-on-primary-fixed hover:bg-primary cursor-pointer">
              <ArrowLeft className="h-4 w-4" />
              <span>Start New Research</span>
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (!results) {
    return null
  }

  const r = results

  // Helper functions
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-status-verified-text bg-status-verified-bg border-status-verified-border'
      case 'partial': return 'text-status-potential-text bg-status-potential-bg border-status-potential-border'
      case 'failed': return 'text-status-conflict-text bg-status-conflict-bg border-status-conflict-border'
      default: return 'text-text-muted bg-surface-container-high border-outline-variant'
    }
  }

  const getCoverageColor = (status: CoverageStatus) => {
    switch (status) {
      case 'covered': return 'text-status-verified-text bg-status-verified-bg border-status-verified-border'
      case 'partial': return 'text-text-primary bg-surface-container-high border-outline-variant'
      case 'missing': return 'text-status-conflict-text bg-status-conflict-bg border-status-conflict-border'
      case 'conflicting': return 'text-status-conflict-text bg-status-conflict-bg border-status-conflict-border'
      case 'outdated': return 'text-status-outdated-text bg-status-outdated-bg border-status-outdated-border'
      case 'weak_evidence': return 'text-status-potential-text bg-status-potential-bg border-status-potential-border'
      default: return 'text-text-muted bg-surface-container-high border-outline-variant'
    }
  }

  const getPriorityColor = (priority: Priority) => {
    switch (priority) {
      case 'critical': return 'text-status-conflict-text bg-status-conflict-bg border-status-conflict-border'
      case 'high': return 'text-status-outdated-text bg-status-outdated-bg border-status-outdated-border'
      case 'medium': return 'text-status-potential-text bg-status-potential-bg border-status-potential-border'
      case 'low': return 'text-status-verified-text bg-status-verified-bg border-status-verified-border'
      default: return 'text-text-muted bg-surface-container-high border-outline-variant'
    }
  }

  const getFindingColor = (status: FindingStatus) => {
    switch (status) {
      case 'verified': return 'text-status-verified-text bg-status-verified-bg border-status-verified-border'
      case 'potential': return 'text-status-potential-text bg-status-potential-bg border-status-potential-border'
      case 'uncertain': return 'text-text-muted bg-surface-container-high border-outline-variant'
      case 'unverified': return 'text-status-conflict-text bg-status-conflict-bg border-status-conflict-border'
      default: return 'text-text-muted bg-surface-container-high border-outline-variant'
    }
  }

  const openEvidenceDrawer = (claim: any) => {
    setSelectedClaim(claim)
    setShowEvidenceDrawer(true)
  }

  return (
    <div className="w-full flex flex-col min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-30 bg-surface-container border-b border-outline-variant px-4 py-3">
        <div className="max-w-[1200px] mx-auto flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <button onClick={() => router.push('/research/new')} className="p-2 rounded-lg hover:bg-surface-container-high transition-colors">
              <ArrowLeft className="h-5 w-5 text-text-secondary" />
            </button>
            <div>
              <h1 className="font-headline-sm text-headline-sm text-on-surface truncate max-w-[400px]">{r.goal.interpretedObjective}</h1>
              <p className="font-data-sm text-data-sm text-on-surface-variant truncate max-w-[400px]">Session: {sessionId?.slice(0, 8)}...</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className={`px-2 py-1 rounded text-data-sm font-medium ${getStatusColor(r.status)}`}>
              {r.status === 'completed' ? 'Completed' : r.status === 'partial' ? 'Partial' : 'Failed'}
            </span>
            {r.completedAt && (
              <span className="font-data-sm text-data-sm text-on-surface-variant">
                Completed {formatRelativeTime(r.completedAt)}
              </span>
            )}
          </div>
        </div>
      </header>

      {/* Evidence Drawer */}
      {showEvidenceDrawer && selectedClaim && (
        <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-end bg-black/50 p-4 sm:p-0" onClick={() => { setShowEvidenceDrawer(false); setSelectedClaim(null); }}>
          <div className="w-full sm:w-[480px] max-h-[90vh] bg-surface-container rounded-t-2xl sm:rounded-xl shadow-2xl overflow-y-auto animate-slide-in" onClick={(e) => e.stopPropagation()}>
            <div className="p-4 sm:p-6 border-b border-outline-variant flex items-center justify-between">
              <h3 className="font-headline-sm text-headline-sm text-on-surface">Evidence Detail</h3>
              <button onClick={() => { setShowEvidenceDrawer(false); setSelectedClaim(null); }} className="p-2 rounded-lg hover:bg-surface-container-high transition-colors">
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="p-4 sm:p-6 space-y-4">
              <div>
                <label className="font-data-sm text-data-sm text-on-surface-variant">Claim</label>
                <p className="font-body-md text-body-md text-on-surface mt-1">{selectedClaim.text}</p>
              </div>
              <div>
                <label className="font-data-sm text-data-sm text-on-surface-variant">Status</label>
                <span className={`inline-block mt-1 px-2 py-1 rounded text-data-sm font-medium ${getFindingColor(selectedClaim.evidenceStatus)}`}>
                  {selectedClaim.evidenceStatus}
                </span>
              </div>
              <div>
                <label className="font-data-sm text-data-sm text-on-surface-variant">Dimension</label>
                <p className="font-body-md text-body-md text-on-surface mt-1">
                  {r.dimensions.find(d => d.id === selectedClaim.dimensionId)?.name || selectedClaim.dimensionId}
                </p>
              </div>
              <div>
                <label className="font-data-sm text-data-sm text-on-surface-variant">Source</label>
                <p className="font-body-md text-body-md text-on-surface mt-1 truncate">
                  {results?.sources.find((s: any) => s.id === selectedClaim.sourceId)?.title || selectedClaim.sourceId}
                </p>
              </div>
              <div>
                <label className="font-data-sm text-data-sm text-on-surface-variant">Supporting Excerpt</label>
                <div className="mt-2 p-3 bg-surface-container-low border border-outline-variant rounded-lg font-body-sm text-body-sm text-on-surface whitespace-pre-wrap">
                  {selectedClaim.excerpt}
                </div>
              </div>
              {selectedClaim.freshness && (
                <div>
                  <label className="font-data-sm text-data-sm text-on-surface-variant">Freshness</label>
                  <span className="inline-block mt-1 px-2 py-1 rounded text-data-sm font-medium bg-surface-container-high border border-outline-variant">
                    {selectedClaim.freshness}
                  </span>
                </div>
              )}
              <div>
                <label className="font-data-sm text-data-sm text-on-surface-variant">Confidence</label>
                <div className="mt-1 flex items-center gap-2">
                  <div className="flex-1 h-2 bg-surface-container-low rounded-full overflow-hidden">
                    <div className="h-full bg-primary-container rounded-full transition-all" style={{ width: `${selectedClaim.confidence * 100}%` }} />
                  </div>
                  <span className="font-data-sm text-data-sm text-on-surface-variant w-12 text-right">
                    {Math.round(selectedClaim.confidence * 100)}%
                  </span>
                </div>
              </div>
            </div>
            <div className="p-4 border-t border-outline-variant flex justify-end gap-2">
              <button onClick={() => { setShowEvidenceDrawer(false); setSelectedClaim(null); }} className="px-4 py-2 rounded-lg font-label-md text-label-md bg-surface-container-high text-on-surface hover:bg-surface-container-highest transition-colors">
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-4 sm:p-6">
        <div className="max-w-[1200px] mx-auto">
          {/* Metrics Bar */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
            <div className="bg-surface-container border border-outline-variant rounded-xl p-4">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-primary-container/20">
                  <FileText className="h-5 w-5 text-primary-container" />
                </div>
                <div>
                  <p className="font-data-sm text-data-sm text-on-surface-variant">Sources</p>
                  <p className="font-headline-sm text-headline-sm text-on-surface font-bold">{r.sources?.length || 0}</p>
                </div>
              </div>
            </div>
            <div className="bg-surface-container border border-outline-variant rounded-xl p-4">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-status-verified-bg/20">
                  <CheckCircle className="h-5 w-5 text-status-verified-text" />
                </div>
                <div>
                  <p className="font-data-sm text-data-sm text-on-surface-variant">Claims</p>
                  <p className="font-headline-sm text-headline-sm text-on-surface font-bold">{r.claims?.length || 0}</p>
                </div>
              </div>
            </div>
            <div className="bg-surface-container border border-outline-variant rounded-xl p-4">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-status-conflict-bg/20">
                  <AlertTriangle className="h-5 w-5 text-status-conflict-text" />
                </div>
                <div>
                  <p className="font-data-sm text-data-sm text-on-surface-variant">Gaps</p>
                  <p className="font-headline-sm text-headline-sm text-on-surface font-bold">{r.gaps?.length || 0}</p>
                </div>
              </div>
            </div>
            <div className="bg-surface-container border border-outline-variant rounded-xl p-4">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-status-conflict-bg/20">
                  <AlertTriangle className="h-5 w-5 text-status-conflict-text" />
                </div>
                <div>
                  <p className="font-data-sm text-data-sm text-on-surface-variant">Conflicts</p>
                  <p className="font-headline-sm text-headline-sm text-on-surface font-bold">{r.conflicts?.length || 0}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="bg-surface-container border border-outline-variant rounded-xl overflow-hidden mb-6">
            <nav className="flex overflow-x-auto" aria-label="Research sections">
              {[
                { id: 'overview', label: 'Overview', icon: <Info className="h-4 w-4" /> },
                { id: 'coverage', label: 'Coverage', icon: <FileText className="h-4 w-4" /> },
                { id: 'gaps', label: 'Gaps', icon: <AlertTriangle className="h-4 w-4" /> },
                { id: 'conflicts', label: 'Conflicts', icon: <AlertTriangle className="h-4 w-4" /> },
                { id: 'sources', label: 'Sources', icon: <Link className="h-4 w-4" /> },
                { id: 'verification', label: 'Verification', icon: <CheckCircle className="h-4 w-4" /> },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 px-4 py-3 whitespace-nowrap font-label-md transition-colors ${
                    activeTab === tab.id
                      ? 'text-primary-container bg-primary-container/10 border-b-2 border-primary-container'
                      : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high'
                  }`}
                >
                  {tab.icon}
                  <span>{tab.label}</span>
                </button>
              ))}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="bg-surface-container border border-outline-variant rounded-xl overflow-hidden">
            {activeTab === 'overview' && (
              <div className="p-6 space-y-6">
                {/* Research Summary */}
                <div className="bg-surface-container-low border border-outline-variant rounded-lg p-5">
                  <h3 className="font-label-md text-label-md text-on-surface mb-2 flex items-center gap-2">
                    <Info className="h-4 w-4 text-primary-container" />
                    Research Summary
                  </h3>
                  <p className="font-body-md text-body-md text-on-surface-variant leading-relaxed">
                    {r.goal.interpretedObjective}
                  </p>
                  <p className="font-data-sm text-data-sm text-on-surface-variant mt-2">
                    Research completed with {r.sources?.length || 0} sources, {r.claims?.length || 0} claims extracted across {r.dimensions?.length || 0} dimensions.
                  </p>
                </div>

                {/* Key Metrics */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div className="bg-surface-container-low border border-outline-variant rounded-lg p-4 text-center">
                    <p className="font-headline-xl text-headline-xl text-primary-container">{r.dimensions?.filter(d => d.coverageStatus === 'covered').length || 0}</p>
                    <p className="font-data-sm text-data-sm text-on-surface-variant mt-1">Dimensions Covered</p>
                  </div>
                  <div className="bg-surface-container-low border border-outline-variant rounded-lg p-4 text-center">
                    <p className="font-headline-xl text-headline-xl text-status-potential-text">{r.dimensions?.filter(d => d.coverageStatus === 'partial').length || 0}</p>
                    <p className="font-data-sm text-data-sm text-on-surface-variant mt-1">Partially Covered</p>
                  </div>
                  <div className="bg-surface-container-low border border-outline-variant rounded-lg p-4 text-center">
                    <p className="font-headline-xl text-headline-xl text-status-conflict-text">{r.dimensions?.filter(d => d.coverageStatus === 'missing').length || 0}</p>
                    <p className="font-data-sm text-data-sm text-on-surface-variant mt-1">Missing</p>
                  </div>
                  <div className="bg-surface-container-low border border-outline-variant rounded-lg p-4 text-center">
                    <p className="font-headline-xl text-headline-xl text-status-conflict-text">{r.conflicts?.length || 0}</p>
                    <p className="font-data-sm text-data-sm text-on-surface-variant mt-1">Conflicts</p>
                  </div>
                </div>

                {/* Quick Actions */}
                <div className="bg-surface-container-low border border-outline-variant rounded-lg p-5">
                  <h3 className="font-label-md text-label-md text-on-surface mb-3 flex items-center gap-2">
                    <ChevronRight className="h-4 w-4 text-primary-container" />
                    Quick Actions
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <button className="px-4 py-3 rounded-lg bg-primary-container text-on-primary-fixed hover:bg-primary transition-colors flex items-center justify-center gap-2 font-label-md">
                      <Download className="h-4 w-4" />
                      <span>Export Report (PDF)</span>
                    </button>
                    <button className="px-4 py-3 rounded-lg bg-surface-container-high text-on-surface hover:bg-surface-container-highest transition-colors flex items-center justify-center gap-2 font-label-md border border-outline-variant">
                      <RefreshCw className="h-4 w-4" />
                      <span>Re-run Research</span>
                    </button>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'coverage' && (
              <div className="p-6 space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">Coverage Analysis</h3>
                  <span className="font-data-sm text-data-sm text-on-surface-variant">
                    {r.dimensions?.filter(d => d.coverageStatus === 'covered').length || 0} / {r.dimensions?.length || 0} dimensions fully covered
                  </span>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-outline-variant">
                        <th className="text-left p-3 font-label-md text-on-surface-variant">Dimension</th>
                        <th className="text-left p-3 font-label-md text-on-surface-variant">Status</th>
                        <th className="text-left p-3 font-label-md text-on-surface-variant">Claims</th>
                        <th className="text-left p-3 font-label-md text-on-surface-variant">Priority</th>
                        <th className="text-left p-3 font-label-md text-on-surface-variant">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {r.dimensions?.map((dim: ResearchDimension) => (
                        <tr key={dim.id} className="border-b border-outline-variant/50 hover:bg-surface-container-low/50">
                          <td className="p-3">
                            <p className="font-body-md text-body-md text-on-surface">{dim.name}</p>
                            <p className="font-data-sm text-data-sm text-on-surface-variant mt-1 truncate max-w-[300px]">{dim.description}</p>
                          </td>
                          <td className="p-3">
                            <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded ${getCoverageColor(dim.coverageStatus || 'missing')}`}>
                              {dim.coverageStatus || 'missing'}
                            </span>
                          </td>
                          <td className="p-3 font-data-sm text-data-sm text-on-surface">{dim.claimCount || 0}</td>
                          <td className="p-3">
                            <span className={`inline-flex items-center gap-1 px-2 py-1 rounded ${(dim.priority ?? 0) >= 4 ? 'text-status-conflict-text bg-status-conflict-bg border-status-conflict-border' : 'text-status-potential-text bg-status-potential-bg border-status-potential-border'}`}>
                              Priority {dim.priority ?? 'N/A'}
                            </span>
                          </td>
                          <td className="p-3">
                            <button className="px-3 py-1.5 rounded bg-surface-container-high text-on-surface hover:bg-surface-container-highest transition-colors font-data-sm text-data-sm flex items-center gap-1">
                              <ChevronRight className="h-3.5 w-3.5" />
                              View
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {activeTab === 'gaps' && (
              <div className="p-6 space-y-4">
                <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-status-conflict-text" />
                  Information Gaps ({r.gaps?.length || 0})
                </h3>
                <div className="space-y-3">
                  {r.gaps?.map((gap: GapResponse) => (
                    <div key={gap.id} className="bg-surface-container-low border border-outline-variant rounded-xl p-5">
                      <div className="flex items-start justify-between gap-4 mb-3">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <h4 className="font-headline-sm text-headline-sm text-on-surface">{gap.title}</h4>
                            <span className={`inline-flex items-center gap-1 px-2 py-1 rounded ${getPriorityColor(gap.priority)}`}>
                              {gap.priority}
                            </span>
                          </div>
                          <p className="font-body-md text-body-md text-on-surface-variant">{gap.explanation}</p>
                        </div>
                        <span className={`inline-flex items-center gap-1 px-2 py-1 rounded ${getPriorityColor(gap.priority)} shrink-0`}>
                          {gap.priority}
                        </span>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                        <div>
                          <p className="font-data-sm text-data-sm text-on-surface-variant">Next Action</p>
                          <p className="font-body-sm text-body-sm text-on-surface mt-1">{gap.nextAction}</p>
                        </div>
                        <div>
                          <p className="font-data-sm text-data-sm text-on-surface-variant">Recommended Authority</p>
                          <p className="font-body-sm text-body-sm text-on-surface mt-1">{gap.recommendedAuthority || '—'}</p>
                        </div>
                        <div>
                          <p className="font-data-sm text-data-sm text-on-surface-variant">Method</p>
                          <p className="font-body-sm text-body-sm text-on-surface mt-1 capitalize">{gap.verificationMethod?.replace('_', ' ') || '—'}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'conflicts' && (
              <div className="p-6 space-y-4">
                <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-status-conflict-text" />
                  Conflicting Claims ({r.conflicts?.length || 0})
                </h3>
                <div className="space-y-4">
                  {r.conflicts?.map((conflict: ConflictResponse) => (
                    <div key={conflict.id} className="bg-surface-container-low border border-outline-variant rounded-xl p-5">
                      <div className="mb-4">
                        <h4 className="font-headline-sm text-headline-sm text-on-surface">
                          {conflict.entity} → {conflict.attribute}
                        </h4>
                        <span className={`inline-flex items-center gap-1 px-2 py-1 rounded text-data-sm font-medium bg-status-conflict-bg/20 border border-status-conflict-border text-status-conflict-text`}>
                          {conflict.conflictType}
                        </span>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-status-conflict-bg/10 border border-status-conflict-border/30 rounded-lg p-4">
                          <div className="flex items-center gap-2 mb-2">
                            <AlertCircle className="h-4 w-4 text-status-conflict-text" />
                            <span className="font-label-md text-label-md text-status-conflict-text">Claim A</span>
                          </div>
                          <p className="font-body-md text-body-md text-on-surface">{conflict.claimA.text}</p>
                          <p className="font-data-sm text-data-sm text-on-surface-variant mt-2">Source: {r.sources?.find(s => s.id === conflict.claimA.sourceId)?.title || conflict.claimA.sourceId}</p>
                          <p className="font-data-sm text-data-sm text-on-surface-variant mt-1">Evidence: {conflict.claimA.exactExcerpt?.slice(0, 150)}...</p>
                        </div>
                        <div className="bg-status-conflict-bg/10 border border-status-conflict-border/30 rounded-lg p-4">
                          <div className="flex items-center gap-2 mb-2">
                            <AlertCircle className="h-4 w-4 text-status-conflict-text" />
                            <span className="font-label-md text-label-md text-status-conflict-text">Claim B</span>
                          </div>
                          <p className="font-body-md text-body-md text-on-surface">{conflict.claimB.text}</p>
                          <p className="font-data-sm text-data-sm text-on-surface-variant mt-2">Source: {r.sources?.find(s => s.id === conflict.claimB.sourceId)?.title || conflict.claimB.sourceId}</p>
                          <p className="font-data-sm text-data-sm text-on-surface-variant mt-1">Evidence: {conflict.claimB.exactExcerpt?.slice(0, 150)}...</p>
                        </div>
                      </div>
                      <div className="mt-4 p-3 bg-surface-container-high rounded-lg border border-outline-variant">
                        <div className="flex items-center gap-2 mb-1">
                          <Info className="h-4 w-4 text-primary-container" />
                          <span className="font-label-md text-label-md text-primary-container">Resolution</span>
                        </div>
                        <p className="font-body-sm text-body-sm text-on-surface-variant">{conflict.resolutionAction || 'Manual verification required'}</p>
                        <p className="font-data-sm text-data-sm text-on-surface-variant mt-1">Confidence: {Math.round(conflict.confidence * 100)}%</p>
                      </div>
                    </div>
                  ))}
                </div>
                {r.conflicts?.length === 0 && (
                  <div className="text-center py-12 bg-surface-container-low border border-outline-variant rounded-xl">
                    <CheckCircle className="h-12 w-12 text-status-verified-text mx-auto mb-4" />
                    <h3 className="font-headline-sm text-headline-sm text-on-surface mb-2">No Conflicts Detected</h3>
                    <p className="font-body-md text-body-md text-on-surface-variant">All claims are consistent across sources.</p>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'sources' && (
              <div className="p-6 space-y-4">
                <h3 className="font-headline-sm text-headline-sm text-on-surface">Sources ({r.sources?.length || 0})</h3>
                <div className="space-y-3">
                  {r.sources?.map((source: SourceResponse) => (
                    <div key={source.id} className="bg-surface-container-low border border-outline-variant rounded-xl p-5 hover:bg-surface-container-high/50 transition-colors">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-2 flex-wrap">
                            <h4 className="font-headline-sm text-headline-sm text-on-surface truncate">{source.title}</h4>
                            <span className={`inline-flex items-center gap-1 px-2 py-1 rounded text-data-sm font-medium ${getStatusColor(source.extractionStatus || 'pending')}`}>
                              {source.extractionStatus || 'pending'}
                            </span>
                          </div>
                          <div className="flex items-center gap-3 flex-wrap text-sm text-on-surface-variant mb-2">
                            <span className="flex items-center gap-1">
                              <Link className="h-3.5 w-3.5" />
                              <span className="truncate max-w-[300px]">{source.url}</span>
                            </span>
                            {source.domain && <span className="flex items-center gap-1"><span className="font-mono">{source.domain}</span></span>}
                            {source.publicationDate && <span className="flex items-center gap-1"><Clock className="h-3.5 w-3.5" /> {formatRelativeTime(source.publicationDate)}</span>}
                          </div>
                          <p className="font-data-sm text-data-sm text-outline mt-2 line-clamp-2">{source.contentPreview}</p>
                        </div>
                        <div className="flex items-center gap-2 shrink-0">
                          <span className={`inline-flex items-center gap-1 px-2 py-1 rounded text-data-sm font-medium ${source.authorityScore > 0.8 ? 'text-status-verified-text bg-status-verified-bg border-status-verified-border' : source.authorityScore > 0.5 ? 'text-status-potential-text bg-status-potential-bg border-status-potential-border' : 'text-text-muted bg-surface-container-high border-outline-variant'}`}>
                            Authority: {Math.round(source.authorityScore * 100)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                {r.sources?.length === 0 && (
                  <div className="text-center py-12 bg-surface-container-low border border-outline-variant rounded-xl">
                    <Link className="h-12 w-12 text-text-muted mx-auto mb-4" />
                    <h3 className="font-headline-sm text-headline-sm text-on-surface mb-2">No Sources</h3>
                    <p className="font-body-md text-body-md text-on-surface-variant">No sources were found or extracted for this research.</p>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'verification' && (
              <div className="p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
                    <CheckCircle className="h-5 w-5 text-status-verified-text" />
                    Verification Checklist ({r.checklist?.filter(t => t.completed).length || 0} / {r.checklist?.length || 0} completed)
                  </h3>
                  <span className="font-data-sm text-data-sm text-on-surface-variant">
                    {r.checklist?.filter(t => t.priority === 'critical').length || 0} critical · {r.checklist?.filter(t => t.priority === 'high').length || 0} high
                  </span>
                </div>
                <div className="space-y-3">
                  {r.checklist?.map((task: VerificationTaskResponse) => (
                    <div key={task.id} className={`bg-surface-container-low border border-outline-variant rounded-xl p-5 transition-colors ${task.completed ? 'opacity-60' : ''}`}>
                      <div className="flex items-start justify-between gap-4 mb-3">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2 flex-wrap">
                            <input
                              type="checkbox"
                              checked={task.completed}
                              onChange={(e) => mockApi.updateChecklistTask(sessionId || 'demo-1', task.id, e.target.checked)}
                              className="w-5 h-5 rounded border-outline-variant text-primary-container focus:ring-2 focus:ring-primary-container"
                            />
                            <h4 className={`font-headline-sm text-headline-sm ${task.completed ? 'line-through text-text-muted' : 'text-on-surface'}`}>{task.title}</h4>
                            <span className={`inline-flex items-center gap-1 px-2 py-1 rounded ${getPriorityColor(task.priority)}`}>
                              {task.priority}
                            </span>
                          </div>
                          <p className="font-body-md text-body-md text-on-surface-variant mb-2">{task.explanation}</p>
                        </div>
                        <div className="flex items-center gap-2 shrink-0">
                          <span className={`inline-flex items-center gap-1 px-2 py-1 rounded ${getPriorityColor(task.priority)} shrink-0`}>
                            {task.priority}
                          </span>
                        </div>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                        <div>
                          <p className="font-data-sm text-data-sm text-on-surface-variant">Why</p>
                          <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">{task.explanation.slice(0, 100)}...</p>
                        </div>
                        <div>
                          <p className="font-data-sm text-data-sm text-on-surface-variant">Authority</p>
                          <p className="font-body-sm text-body-sm text-on-surface mt-1 truncate max-w-[200px]">{task.recommendedAuthority || '—'}</p>
                        </div>
                        <div>
                          <p className="font-data-sm text-data-sm text-on-surface-variant">Method</p>
                          <p className="font-body-sm text-body-sm text-on-surface mt-1 capitalize">{task.verificationMethod?.replace('_', ' ') || '—'}</p>
                        </div>
                      </div>
                      <div className="mt-3 flex items-center gap-2">
                        <a href={r.sources?.find(s => task.sourceIds?.includes(s.id))?.url || '#'} target="_blank" rel="noopener noreferrer" className="px-3 py-1.5 rounded bg-primary-container text-on-primary-fixed hover:bg-primary transition-colors font-data-sm text-data-sm flex items-center gap-1">
                          <Link className="h-3.5 w-3.5" />
                          <span>Open Source</span>
                        </a>
                        <button className="px-3 py-1.5 rounded bg-surface-container-high text-on-surface hover:bg-surface-container-highest transition-colors font-data-sm text-data-sm flex items-center gap-1">
                          <Clock className="h-3.5 w-3.5" />
                          <span>Est. {task.verificationMethod === 'official_source' ? '5 min' : '15 min'}</span>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
                {r.checklist?.length === 0 && (
                  <div className="text-center py-12 bg-surface-container-low border border-outline-variant rounded-xl">
                    <CheckCircle className="h-12 w-12 text-status-verified-text mx-auto mb-4" />
                    <h3 className="font-headline-sm text-headline-sm text-on-surface mb-2">All Clear!</h3>
                    <p className="font-body-md text-body-md text-on-surface-variant">No verification tasks needed.</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="mt-8 pt-6 border-t border-outline-variant flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="font-data-sm text-data-sm text-on-surface-variant">
              GapLens Core v1.4 · Research completed {formatRelativeTime(r.completedAt || new Date().toISOString())}
            </p>
            <div className="flex items-center gap-2">
              <button onClick={() => router.push('/research/new')} className="px-4 py-2 rounded-lg font-label-md text-label-md bg-surface-container-high text-on-surface hover:bg-surface-container-highest transition-colors flex items-center gap-2">
                <ArrowLeft className="h-4 w-4" />
                <span>New Research</span>
              </button>
              <button className="px-4 py-2 rounded-lg font-label-md text-label-md font-medium transition-all duration-150 flex items-center justify-center gap-2 bg-primary-container text-on-primary-fixed hover:bg-primary cursor-pointer">
                <Download className="h-4 w-4" />
                <span>Export Report</span>
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}