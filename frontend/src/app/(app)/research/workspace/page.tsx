'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function ResearchWorkspacePage() {
  const router = useRouter()

  useEffect(() => {
    // Redirect back to new research if accessed directly
    // In real app, this would show the research results
    const timer = setTimeout(() => {
      router.push('/research/new')
    }, 2000)
    return () => clearTimeout(timer)
  }, [router])

  return (
    <div className="w-full flex flex-col items-center justify-center px-4 py-8 md:py-12 select-none min-h-screen bg-background">
      <div className="w-full max-w-[760px] text-center">
        <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded bg-surface-container-high border border-outline-variant mb-4">
          <span className="w-1.5 h-1.5 rounded-full bg-primary-container"></span>
          <span className="font-data-sm text-data-sm text-on-surface-variant uppercase tracking-wider">GapLens Core v1.4</span>
        </div>
        <h1 className="font-headline-xl text-headline-xl text-on-surface tracking-tight mb-4">
          Research Workspace
        </h1>
        <p className="font-body-md text-body-md text-on-surface-variant max-w-[580px] mx-auto">
          This is where your research results would appear. The pipeline would run through:
        </p>
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
          {[
            'Goal Understanding',
            'Research Dimensions',
            'Query Planning',
            'Parallel Web Search',
            'Source Ingestion',
            'Claim Extraction',
            'Evidence Analysis',
            'Gap Prioritization',
            'Verification Planning'
          ].map((stage, i) => (
            <div key={stage} className="bg-surface-container border border-outline-variant rounded-lg p-4 flex items-center gap-3">
              <span className="font-data-sm text-data-sm text-primary-container font-mono w-8 text-center">{i + 1}</span>
              <span className="font-body-md text-body-md text-on-surface">{stage}</span>
            </div>
          ))}
        </div>
        <div className="mt-8">
          <button
            onClick={() => router.push('/research/new')}
            className="w-full sm:w-auto px-6 py-2.5 rounded-lg font-label-md text-label-md font-medium transition-all duration-150 flex items-center justify-center gap-2 bg-primary-container text-on-primary-fixed hover:bg-primary cursor-pointer mx-auto"
          >
            <span className="material-symbols-outlined text-[18px]">arrow_back</span>
            <span>Start New Research</span>
          </button>
        </div>
      </div>
    </div>
  )
}