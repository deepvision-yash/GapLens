'use client'

import Link from 'next/link'
import { clsx } from 'clsx'
import { formatRelativeTime } from '@/lib/utils'
import { ResearchSession, SessionStatus, STATUS_LABELS } from '@/types/research'
import { Clock, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'

interface RecentResearchListProps {
  sessions: ResearchSession[]
  emptyMessage?: string
}

const statusIcons = {
  completed: CheckCircle,
  partial: AlertCircle,
  failed: AlertCircle,
  searching: Loader2,
  extracting: Loader2,
  analyzing: Loader2,
  claim_extraction: Loader2,
  generating_checklist: Loader2,
  understanding: Loader2,
  scope_review: Loader2,
  ready: Loader2,
  created: Clock,
}

const statusColors = {
  completed: 'text-status-verified-text',
  partial: 'text-status-potential-text',
  failed: 'text-status-conflict-text',
  searching: 'text-accent-DEFAULT',
  extracting: 'text-accent-DEFAULT',
  analyzing: 'text-accent-DEFAULT',
  claim_extraction: 'text-accent-DEFAULT',
  generating_checklist: 'text-accent-DEFAULT',
  understanding: 'text-accent-DEFAULT',
  scope_review: 'text-accent-DEFAULT',
  ready: 'text-text-muted',
  created: 'text-text-muted',
}

export function RecentResearchList({ sessions, emptyMessage = 'No recent research sessions. Start your first investigation above.' }: RecentResearchListProps) {
  if (sessions.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">
          <Clock className="h-10 w-10" aria-hidden="true" />
        </div>
        <p className="text-body text-text-secondary">{emptyMessage}</p>
      </div>
    )
  }

  return (
    <section aria-labelledby="recent-heading">
      <div className="flex items-center justify-between mb-4">
        <h2 id="recent-heading" className="section font-semibold text-text-primary">
          Recent research
        </h2>
        <Link
          href="/history"
          className="text-body-sm text-accent-DEFAULT hover:text-accent-hover font-medium transition-colors"
        >
          View all
        </Link>
      </div>

      <div className="space-y-2" role="list">
        {sessions.slice(0, 5).map((session) => {
          const StatusIcon = statusIcons[session.status] || Clock
          const statusColor = statusColors[session.status] || 'text-text-muted'

          return (
            <Link
              key={session.id}
              href={`/research/${session.id}`}
              className={clsx(
                'flex items-center gap-3 p-3 bg-canvas-elevated border border-border-subtle rounded-surface',
                'hover:bg-canvas-raised hover:border-border-DEFAULT transition-colors duration-fast',
                'focus-visible:ring-2 focus-visible:ring-accent-DEFAULT focus-visible:ring-offset-2 focus-visible:ring-offset-canvas-DEFAULT'
              )}
              role="listitem"
            >
              <div className={clsx('p-2 rounded-control bg-canvas-raised', statusColor)}>
                <StatusIcon className="h-4 w-4" aria-hidden="true" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-body font-medium text-text-primary truncate">{session.title}</p>
                <div className="flex items-center gap-3 mt-1">
                  <span className="text-meta text-text-muted">{formatRelativeTime(session.updatedAt)}</span>
                  <span className={clsx('text-meta font-medium', statusColor)}>
                    {STATUS_LABELS[session.status]}
                  </span>
                  {session.sourceCount !== undefined && (
                    <span className="text-meta text-text-muted">{session.sourceCount} sources</span>
                  )}
                </div>
              </div>
            </Link>
          )
        })}
      </div>
    </section>
  )
}