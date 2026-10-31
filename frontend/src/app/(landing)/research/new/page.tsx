'use client'

import { useState, useRef, useEffect, FormEvent } from 'react'
import { useRouter } from 'next/navigation'

export default function ResearchNewPage() {
  const router = useRouter()
  const topicInputRef = useRef<HTMLTextAreaElement>(null)
  const urlInputRef = useRef<HTMLInputElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const urlInputGroupRef = useRef<HTMLDivElement>(null)
  const submitBtnRef = useRef<HTMLButtonElement>(null)
  const charCounterRef = useRef<HTMLSpanElement>(null)

  const [topic, setTopic] = useState('')
  const [charCount, setCharCount] = useState(0)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [urlItems, setUrlItems] = useState<Array<{id: number, url: string}>>([
    { id: Date.now(), url: 'https://gate2025.iitr.ac.in/eligibility' }
  ])
  const [docItems, setDocItems] = useState<Array<{id: number, name: string, size: string}>>([
    { id: Date.now() + 1, name: 'official_brochure_gate_2025.pdf', size: '2.4 MB' }
  ])
  const [showUrlInput, setShowUrlInput] = useState(false)
  const [newUrl, setNewUrl] = useState('')

  const MAX_CHARS = 280

  useEffect(() => {
    updateSubmitButton()
    updateCharCounter()
  }, [topic, isSubmitting])

  const updateSubmitButton = () => {
    const btn = submitBtnRef.current
    if (!btn) return
    
    if (topic.trim().length > 0 && !isSubmitting) {
      btn.disabled = false
      btn.className = 'w-full sm:w-auto px-6 py-2.5 rounded-lg font-label-md text-label-md font-medium transition-all duration-150 flex items-center justify-center gap-2 bg-primary-container text-on-primary-fixed hover:bg-primary cursor-pointer'
    } else {
      btn.disabled = true
      btn.className = 'w-full sm:w-auto px-6 py-2.5 rounded-lg font-label-md text-label-md font-medium transition-all duration-150 flex items-center justify-center gap-2 bg-surface-container-high text-outline cursor-not-allowed'
    }
  }

  const updateCharCounter = () => {
    if (charCounterRef.current) {
      charCounterRef.current.textContent = `${topic.length} / ${MAX_CHARS}`
    }
  }

  const handleTopicChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value
    setTopic(value)
    setCharCount(value.length)
  }

  const handleSuggestTopic = () => {
    const suggested = 'GATE 2025 eligibility criteria, reservation policies, and application deadlines'
    setTopic(suggested)
    setCharCount(suggested.length)
    topicInputRef.current?.focus()
  }

  const toggleUrlInput = () => {
    setShowUrlInput(prev => !prev)
    setTimeout(() => { if (!showUrlInput) urlInputRef.current?.focus() }, 0)
  }

  const addUrlItem = () => {
    const val = newUrl.trim()
    if (!val) return
    
    try {
      new URL(val)
    } catch {
      alert('Please enter a valid URL')
      return
    }

    setUrlItems(prev => [...prev, { id: Date.now(), url: val }])
    setNewUrl('')
    setShowUrlInput(false)
  }

  const removeUrlItem = (id: number) => {
    setUrlItems(prev => prev.filter(item => item.id !== id))
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
    if (!allowedTypes.includes(file.type) && !file.name.endsWith('.txt')) {
      alert('Only PDF, DOCX, and TXT files are allowed')
      return
    }

    const sizeFormatted = (file.size / (1024 * 1024)).toFixed(1) + ' MB'
    setDocItems(prev => [...prev, { 
      id: Date.now(), 
      name: file.name, 
      size: sizeFormatted 
    }])
    
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const removeDocItem = (id: number) => {
    setDocItems(prev => prev.filter(item => item.id !== id))
  }

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (topic.trim().length === 0 || isSubmitting) return

    setIsSubmitting(true)
    const btn = submitBtnRef.current
    if (btn) {
      btn.innerHTML = `
        <span class="material-symbols-outlined text-[18px] animate-spin">progress_activity</span>
        <span>Initializing Engine...</span>
      `
      btn.disabled = true
    }

    setTimeout(() => {
      router.push('/research/workspace')
    }, 600)
  }

  const handleUrlKeydown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      addUrlItem()
    }
  }

  return (
    <div className="w-full flex flex-col items-center justify-center px-4 py-8 md:py-12 select-none min-h-screen bg-background">
      <div className="w-full max-w-[760px] text-center mb-7">
        <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded bg-surface-container-high border border-outline-variant mb-4">
          <span className="w-1.5 h-1.5 rounded-full bg-primary-container" aria-hidden="true"></span>
          <span className="font-data-sm text-data-sm text-on-surface-variant uppercase tracking-wider">GapLens Core v1.4</span>
        </div>
        <h1 className="font-headline-xl text-headline-xl text-on-surface tracking-tight">
          What do you want to investigate?
        </h1>
        <p className="font-body-md text-body-md text-on-surface-variant mt-2 max-w-[580px] mx-auto">
          Find missing information, uncover conflicting claims, and discover what needs verification across heterogeneous sources.
        </p>
      </div>
      
      <form onSubmit={handleSubmit} className="w-full max-w-[760px] bg-surface-container border border-outline-variant rounded-2xl p-6 md:p-7 shadow-sm">
        <div className="flex flex-col">
          {/* Research Topic */}
          <div className="flex items-center justify-between mb-2">
            <label className="font-label-md text-label-md text-on-surface flex items-center gap-1" htmlFor="topic-input">
              Research Topic <span className="text-primary-container font-mono">*</span>
            </label>
            <span ref={charCounterRef} className="font-data-sm text-data-sm text-outline" id="char-counter">
              {charCount} / {MAX_CHARS}
            </span>
          </div>
          <div className="relative">
            <textarea
              ref={topicInputRef}
              id="topic-input"
              value={topic}
              onChange={handleTopicChange}
              placeholder="e.g. GATE 2025 eligibility criteria and application process"
              rows={3}
              className="w-full bg-[#242526] border border-outline-variant rounded-lg p-4 font-body-md text-body-md text-on-surface placeholder:text-outline focus:outline-none focus:border-primary-container transition-colors resize-none"
              maxLength={MAX_CHARS}
            />
            <div className="absolute right-3 bottom-3 flex items-center gap-1.5">
              <button
                type="button"
                id="suggest-topic-btn"
                onClick={handleSuggestTopic}
                className="font-data-sm text-data-sm px-2 py-1 rounded bg-surface-container-high hover:bg-surface-container-highest text-on-surface-variant hover:text-on-surface transition-colors border border-outline-variant flex items-center gap-1"
              >
                <span className="material-symbols-outlined text-[13px]" aria-hidden="true">lightbulb</span>
                <span>Sample topic</span>
              </button>
            </div>
          </div>

          {/* Automatic Web Research - Included */}
          <div className="mt-3 bg-surface-container-low border border-outline-variant rounded-lg px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2.5 min-w-0">
              <span className="material-symbols-outlined text-[18px] text-primary-container shrink-0" aria-hidden="true">public</span>
              <div className="flex items-baseline gap-2 truncate">
                <span className="font-label-md text-label-md text-on-surface whitespace-nowrap">Automatic Web Research</span>
                <span className="font-body-sm text-body-sm text-outline truncate hidden sm:inline">
                  GapLens automatically discovers relevant sources for your topic.
                </span>
              </div>
            </div>
            <span className="font-data-sm text-data-sm bg-surface-container-high text-primary-container border border-outline-variant px-2 py-0.5 rounded font-mono uppercase tracking-wider shrink-0 ml-3">
              Included
            </span>
          </div>

          {/* Additional Sources (Optional) */}
          <div className="mt-6 mb-3">
            <span className="font-data-sm text-data-sm uppercase tracking-widest text-outline font-medium">
              Additional Sources (Optional)
            </span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {/* Add URLs */}
            <div className="bg-surface-container-low border border-outline-variant rounded-lg p-4 flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="material-symbols-outlined text-[18px] text-primary-container" aria-hidden="true">link</span>
                  <span className="font-headline-sm text-headline-sm text-on-surface">Add URLs</span>
                </div>
                <p className="font-body-sm text-body-sm text-outline">
                  Include websites, articles, and reference links for corroboration.
                </p>
                <div className="mt-3 flex flex-col gap-2" id="url-items-container">
                  {urlItems.map((item) => (
                    <div key={item.id} id={`url-item-${item.id}`} className="flex items-center justify-between px-2.5 py-1.5 rounded bg-surface-container border border-outline-variant">
                      <div className="flex items-center gap-2 min-w-0 pr-2">
                        <span className="material-symbols-outlined text-[14px] text-outline" aria-hidden="true">language</span>
                        <span className="font-data-sm text-data-sm text-secondary-fixed-dim truncate">{item.url}</span>
                      </div>
                      <div className="flex items-center gap-2 shrink-0">
                        <span className="font-data-sm text-data-sm text-primary-container font-mono hidden sm:inline">Ready to crawl</span>
                        <button
                          type="button"
                          onClick={() => removeUrlItem(item.id)}
                          className="text-outline hover:text-error transition-colors flex items-center"
                        >
                          <span className="material-symbols-outlined text-[16px]" aria-hidden="true">close</span>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
                <div className={`mt-2 flex items-center gap-1.5 ${showUrlInput ? '' : 'hidden'}`} id="url-input-group" ref={urlInputGroupRef}>
                  <input
                    ref={urlInputRef}
                    type="url"
                    id="url-input-field"
                    value={newUrl}
                    onChange={(e) => setNewUrl(e.target.value)}
                    onKeyDown={handleUrlKeydown}
                    placeholder="https://..."
                    className="flex-1 bg-surface-container border border-outline-variant rounded px-2.5 py-1.5 font-data-sm text-data-sm text-on-surface placeholder:text-outline focus:outline-none focus:border-primary-container"
                  />
                  <button
                    type="button"
                    id="confirm-add-url"
                    onClick={addUrlItem}
                    className="bg-surface-container-high hover:bg-surface-container-highest text-on-surface border border-outline-variant font-data-sm text-data-sm px-2.5 py-1.5 rounded"
                  >
                    Add
                  </button>
                </div>
              </div>
              <div className="mt-3 pt-2">
                <button
                  type="button"
                  id="toggle-url-input-btn"
                  onClick={toggleUrlInput}
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-3 py-1.5 rounded bg-surface-container-high hover:bg-surface-container-highest border border-outline-variant font-label-md text-label-md text-on-surface transition-colors"
                >
                  <span className="material-symbols-outlined text-[15px]" aria-hidden="true">add</span>
                  <span>Add URL</span>
                </button>
              </div>
            </div>

            {/* Upload Documents */}
            <div className="bg-surface-container-low border border-outline-variant rounded-lg p-4 flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="material-symbols-outlined text-[18px] text-primary-container" aria-hidden="true">description</span>
                  <span className="font-headline-sm text-headline-sm text-on-surface">Upload Documents</span>
                </div>
                <p className="font-body-sm text-body-sm text-outline">
                  Attach local primary research PDFs, policy drafts, or filings.
                </p>
                <div className="mt-3 flex flex-col gap-2" id="document-items-container">
                  {docItems.map((item) => (
                    <div key={item.id} id={`doc-item-${item.id}`} className="flex items-center justify-between px-2.5 py-1.5 rounded bg-surface-container border border-outline-variant">
                      <div className="flex items-center gap-2 min-w-0 pr-2">
                        <span className="material-symbols-outlined text-[14px] text-outline" aria-hidden="true">picture_as_pdf</span>
                        <span className="font-data-sm text-data-sm text-on-surface truncate">{item.name}</span>
                        <span className="font-data-sm text-data-sm text-outline font-mono hidden sm:inline">{item.size}</span>
                      </div>
                      <button
                        type="button"
                        onClick={() => removeDocItem(item.id)}
                        className="text-outline hover:text-error transition-colors flex items-center shrink-0"
                      >
                        <span className="material-symbols-outlined text-[16px]" aria-hidden="true">close</span>
                      </button>
                    </div>
                  ))}
                </div>
              </div>
              <div className="mt-3 pt-2">
                <label className="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-3 py-1.5 rounded bg-surface-container-high hover:bg-surface-container-highest border border-outline-variant font-label-md text-label-md text-on-surface transition-colors cursor-pointer">
                  <span className="material-symbols-outlined text-[15px]" aria-hidden="true">upload_file</span>
                  <span>Choose Document</span>
                  <input
                    ref={fileInputRef}
                    accept=".pdf,.docx,.txt"
                    type="file"
                    onChange={handleFileChange}
                    className="hidden"
                    id="file-uploader"
                  />
                </label>
                <div className="mt-2 font-data-sm text-data-sm text-outline">
                  PDF, DOCX, TXT (up to 25MB)
                </div>
              </div>
            </div>
          </div>

          {/* Submit */}
          <div className="mt-7 pt-5 border-t border-outline-variant flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-2 text-outline font-body-sm text-body-sm">
              <span className="material-symbols-outlined text-[16px] text-outline" aria-hidden="true">verified</span>
              <span>All your sources are combined into one research workspace.</span>
            </div>
            <button
              ref={submitBtnRef}
              type="submit"
              id="submit-research-btn"
              disabled={topic.trim().length === 0 || isSubmitting}
              className={topic.trim().length > 0 && !isSubmitting
                ? 'w-full sm:w-auto px-6 py-2.5 rounded-lg font-label-md text-label-md font-medium transition-all duration-150 flex items-center justify-center gap-2 bg-primary-container text-on-primary-fixed hover:bg-primary cursor-pointer'
                : 'w-full sm:w-auto px-6 py-2.5 rounded-lg font-label-md text-label-md font-medium transition-all duration-150 flex items-center justify-center gap-2 bg-surface-container-high text-outline cursor-not-allowed'
              }
            >
              <span>{isSubmitting ? 'Initializing Engine...' : 'Start Research'}</span>
              <span className="material-symbols-outlined text-[18px]" aria-hidden="true">{isSubmitting ? 'progress_activity' : 'arrow_forward'}</span>
            </button>
          </div>
        </div>
      </form>

      {/* Feature badges & latency */}
      <div className="w-full max-w-[760px] mt-6 flex flex-wrap items-center justify-between gap-3 px-2 font-data-sm text-data-sm text-outline">
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-outline-variant" aria-hidden="true"></span> Cross-document synthesis</span>
          <span className="flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-outline-variant" aria-hidden="true"></span> Conflict detection</span>
          <span className="flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-outline-variant" aria-hidden="true"></span> Automated gap matrix</span>
        </div>
        <div className="font-mono text-outline">
          {'LATENCY: <1.2s / SOURCE'}
        </div>
      </div>
    </div>
  )
}