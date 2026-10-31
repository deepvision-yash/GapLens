'use client'

import { useState, useCallback } from 'react'
import { X, Link as LinkIcon, FileText, Loader2, CheckCircle, AlertCircle } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/Button'
import { SourceInput } from '@/types/research'

interface SourceChipsProps {
  sources: SourceInput[]
  onRemove: (index: number) => void
  onAddUrl: (url: string) => void
  onAddFile: (file: File) => void
  maxSources?: number
}

export function SourceChips({ sources, onRemove, onAddUrl, onAddFile, maxSources = 10 }: SourceChipsProps) {
  const [urlInput, setUrlInput] = useState('')
  const [urlError, setUrlError] = useState('')
  const [isValidatingUrl, setIsValidatingUrl] = useState(false)
  const [fileInputKey, setFileInputKey] = useState(0)
  const [uploadingFiles, setUploadingFiles] = useState<Set<number>>(new Set())

  const validateUrl = (url: string): boolean => {
    try {
      const parsed = new URL(url)
      return parsed.protocol === 'http:' || parsed.protocol === 'https:'
    } catch {
      return false
    }
  }

  const handleUrlSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!urlInput.trim()) return

    if (!validateUrl(urlInput)) {
      setUrlError('Please enter a valid HTTP/HTTPS URL')
      return
    }

    setIsValidatingUrl(true)
    setUrlError('')

    // Simulate URL validation
    setTimeout(() => {
      onAddUrl(urlInput.trim())
      setUrlInput('')
      setIsValidatingUrl(false)
    }, 500)
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    if (files.length === 0) return

    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
    const validFiles = files.filter(f => validTypes.includes(f.type) || f.name.endsWith('.txt'))

    validFiles.forEach((file, index) => {
      const fileId = Date.now() + index
      setUploadingFiles(prev => new Set([...prev, fileId]))

      // Simulate upload
      setTimeout(() => {
        onAddFile(file)
        setUploadingFiles(prev => {
          const next = new Set(prev)
          next.delete(fileId)
          return next
        })
      }, 800)
    })

    // Reset file input
    setFileInputKey(prev => prev + 1)
  }

  const canAddMore = sources.length < maxSources

  return (
    <div className="space-y-3">
      {/* Existing source chips */}
      {sources.length > 0 && (
        <div className="flex flex-wrap gap-2" role="list" aria-label="Attached sources">
          {sources.map((source, index) => (
            <div
              key={index}
              className={cn(
                'flex items-center gap-2 px-3 py-1.5 bg-canvas-elevated border border-border-DEFAULT rounded-control',
                source.kind === 'file' && 'bg-canvas-raised'
              )}
              role="listitem"
            >
              {source.kind === 'url' ? (
                <LinkIcon className="h-3.5 w-3.5 text-text-muted flex-shrink-0" aria-hidden="true" />
              ) : (
                <FileText className="h-3.5 w-3.5 text-text-muted flex-shrink-0" aria-hidden="true" />
              )}
              <span className="text-body-sm text-text-primary truncate max-w-[200px]" title={source.kind === 'url' ? source.url : source.file?.name}>
                {source.kind === 'url' ? source.url : source.file?.name}
              </span>
              <button
                type="button"
                onClick={() => onRemove(index)}
                className="flex-shrink-0 p-1 text-text-muted hover:text-text-primary hover:bg-canvas-DEFAULT rounded-control transition-colors"
                aria-label={`Remove ${source.kind === 'url' ? 'URL' : 'file'}`}
              >
                <X className="h-3.5 w-3.5" aria-hidden="true" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Add URL */}
      {canAddMore && (
        <form onSubmit={handleUrlSubmit} className="flex gap-2">
          <div className="flex-1 relative">
            <input
              type="url"
              value={urlInput}
              onChange={(e) => {
                setUrlInput(e.target.value)
                if (urlError) setUrlError('')
              }}
              onBlur={() => {
                if (urlInput.trim() && !validateUrl(urlInput)) {
                  setUrlError('Please enter a valid HTTP/HTTPS URL')
                }
              }}
              placeholder="Add a URL (optional)"
              className={cn(
                'w-full px-3.5 py-2.5 pl-10 bg-canvas-elevated border rounded-control text-text-primary placeholder-text-muted',
                'transition-colors duration-fast',
                'focus:border-accent-DEFAULT focus:ring-2 focus:ring-accent-muted focus:outline-none',
                urlError ? 'border-status-conflict-border' : 'border-border-DEFAULT hover:border-border-DEFAULT/80'
              )}
              disabled={isValidatingUrl || !canAddMore}
              aria-invalid={urlError ? 'true' : 'false'}
              aria-describedby={urlError ? 'url-error' : undefined}
            />
            <LinkIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-muted" aria-hidden="true" />
          </div>
          <Button type="submit" disabled={!urlInput.trim() || isValidatingUrl || !canAddMore} size="md">
            {isValidatingUrl ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Add'}
          </Button>
        </form>
      )}

      {urlError && (
        <p id="url-error" className="text-body-sm text-status-conflict-text" role="alert">
          {urlError}
        </p>
      )}

      {/* File upload */}
      {canAddMore && (
        <div className="relative">
          <input
            type="file"
            key={fileInputKey}
            onChange={handleFileChange}
            accept=".pdf,.docx,.txt"
            multiple
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            aria-label="Upload documents"
            disabled={!canAddMore}
          />
          <Button
            variant="secondary"
            className="w-full justify-center gap-2"
            disabled={!canAddMore}
            type="button"
          >
            <FileText className="h-4 w-4" aria-hidden="true" />
            <span>Upload PDF, DOCX, or TXT</span>
            {uploadingFiles.size > 0 && (
              <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
            )}
          </Button>
        </div>
      )}

      {!canAddMore && (
        <p className="text-body-sm text-text-muted text-center">
          Maximum of {maxSources} sources reached
        </p>
      )}

      <p className="text-body-sm text-text-muted text-center">
        Adding sources is optional. Automatic web research is included.
      </p>
    </div>
  )
}