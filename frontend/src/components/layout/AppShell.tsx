'use client'

import { ReactNode, useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { clsx } from 'clsx'
import {
  Search,
  History,
  Database,
  ClipboardList,
  Settings,
  HelpCircle,
  Menu,
  X,
  ChevronLeft,
  Plus,
  Sparkles,
} from 'lucide-react'

const navigation = [
  { name: 'Home', href: '/', icon: Search },
  { name: 'History', href: '/history', icon: History },
  { name: 'Sources', href: '/sources', icon: Database },
  { name: 'Verifications', href: '/verifications', icon: ClipboardList },
]

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  return (
    <div className="flex h-screen bg-canvas-DEFAULT overflow-hidden">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        className={clsx(
          'fixed lg:static inset-y-0 left-0 z-50 flex flex-col bg-canvas-elevated border-r border-border-subtle transition-all duration-normal',
          sidebarCollapsed ? 'w-16' : 'w-64',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        )}
        aria-label="Main navigation"
      >
        {/* Logo & Brand */}
        <div className={clsx('flex items-center gap-3 p-4 border-b border-border-subtle', sidebarCollapsed && 'justify-center')}>
          <Link href="/" className="flex items-center gap-2" aria-label="GapLens Home">
            <div className="relative flex h-8 w-8 items-center justify-center rounded-control bg-accent-DEFAULT">
              <Sparkles className="h-5 w-5 text-white" aria-hidden="true" />
            </div>
            {!sidebarCollapsed && (
              <span className="font-semibold text-lg text-text-primary">GapLens</span>
            )}
          </Link>
          {!sidebarCollapsed && (
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="ml-auto btn-icon text-text-muted hover:text-text-primary"
              aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
              aria-expanded={!sidebarCollapsed}
            >
              {sidebarCollapsed ? <ChevronLeft className="h-4 w-4" /> : <X className="h-4 w-4" />}
            </button>
          )}
        </div>

        {/* Primary Action - New Research */}
        {!sidebarCollapsed && (
          <div className="p-4">
            <Link
              href="/research/new"
              className={clsx(
                'w-full btn-primary justify-center',
                pathname === '/research/new' && 'bg-accent-hover'
              )}
            >
              <Plus className="h-4 w-4" aria-hidden="true" />
              <span>New Research</span>
            </Link>
          </div>
        )}

        {/* Navigation */}
        <nav className="flex-1 px-3 py-2 space-y-1" aria-label="Primary">
          <ul className="space-y-1" role="list">
            {navigation.map((item) => {
              const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href))
              return (
                <li key={item.name}>
                  <Link
                    href={item.href}
                    className={clsx(
                      'flex items-center gap-3 px-3 py-2.5 rounded-control text-body-sm font-medium transition-colors duration-fast',
                      isActive
                        ? 'bg-accent-muted text-accent-DEFAULT'
                        : 'text-text-secondary hover:bg-canvas-raised hover:text-text-primary',
                      sidebarCollapsed && 'justify-center px-2'
                    )}
                    aria-current={isActive ? 'page' : undefined}
                    title={sidebarCollapsed ? item.name : undefined}
                  >
                    <item.icon className="h-4 w-4 flex-shrink-0" aria-hidden="true" />
                    {!sidebarCollapsed && <span>{item.name}</span>}
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>

        {/* Bottom section */}
        <div className={clsx('p-3 border-t border-border-subtle', sidebarCollapsed && 'px-2')}>
          <ul className="space-y-1" role="list">
            {[
              { name: 'Settings', href: '/settings', icon: Settings },
              { name: 'Help', href: '/help', icon: HelpCircle },
            ].map((item) => (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className={clsx(
                    'flex items-center gap-3 px-3 py-2 rounded-control text-body-sm text-text-muted hover:bg-canvas-raised hover:text-text-primary transition-colors duration-fast',
                    sidebarCollapsed && 'justify-center px-2'
                  )}
                  title={sidebarCollapsed ? item.name : undefined}
                >
                  <item.icon className="h-4 w-4 flex-shrink-0" aria-hidden="true" />
                  {!sidebarCollapsed && <span>{item.name}</span>}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </aside>

      {/* Main content area */}
      <div className="flex-1 flex flex-col min-w-0 lg:ml-0">
        {/* Mobile menu button + Top bar */}
        <header className="sticky top-0 z-30 flex items-center gap-4 px-4 py-3 bg-canvas-elevated/80 backdrop-blur-sm border-b border-border-subtle lg:px-6">
          <button
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden btn-icon text-text-secondary hover:text-text-primary"
            aria-label="Open navigation"
            aria-expanded={sidebarOpen}
            aria-controls="sidebar"
          >
            <Menu className="h-5 w-5" aria-hidden="true" />
          </button>

          <div className="flex-1" />

          {/* Contextual actions would go here */}
        </header>

        {/* Main content */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-6 xl:p-8">
          <div className="mx-auto max-w-dashboard">{children}</div>
        </main>
      </div>
    </div>
  )
}