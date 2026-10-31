'use client'

import { forwardRef, ButtonHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'icon'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', loading, disabled, children, ...props }, ref) => {
    const baseStyles = 'inline-flex items-center justify-center gap-2 font-medium rounded-control transition-colors duration-fast focus-visible:ring-2 focus-visible:ring-accent-DEFAULT focus-visible:ring-offset-2 focus-visible:ring-offset-canvas-DEFAULT disabled:opacity-50 disabled:cursor-not-allowed'

    const variants = {
      primary: 'bg-accent-DEFAULT text-white hover:bg-accent-hover',
      secondary: 'bg-canvas-raised text-text-primary border border-border-DEFAULT hover:bg-canvas-overlay',
      ghost: 'bg-transparent text-text-secondary hover:bg-canvas-elevated hover:text-text-primary',
      danger: 'bg-status-conflict-bg text-status-conflict-text border border-status-conflict-border hover:bg-status-conflict-border',
      icon: 'p-2',
    }

    const sizes = {
      sm: 'px-3 py-1.5 text-body-sm',
      md: 'px-4 py-2.5 text-body-sm',
      lg: 'px-5 py-3 text-body',
    }

    return (
      <button
        ref={ref}
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" aria-hidden="true">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        )}
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'