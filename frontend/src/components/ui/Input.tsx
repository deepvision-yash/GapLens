'use client'

import { forwardRef, InputHTMLAttributes, TextareaHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, helperText, id, ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-')

    return (
      <div className="w-full">
        {label && (
          <label htmlFor={inputId} className="block text-body-sm font-medium text-text-primary mb-1.5">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={cn(
            'w-full px-3.5 py-2.5 bg-canvas-elevated border rounded-control text-text-primary placeholder-text-muted',
            'transition-colors duration-fast',
            'focus:border-accent-DEFAULT focus:ring-2 focus:ring-accent-muted focus:outline-none',
            'disabled:bg-canvas-elevated/50 disabled:cursor-not-allowed',
            error
              ? 'border-status-conflict-border focus:border-status-conflict-DEFAULT focus:ring-status-conflict-muted'
              : 'border-border-DEFAULT hover:border-border-DEFAULT/80',
            className
          )}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined}
          {...props}
        />
        {error && (
          <p id={`${inputId}-error`} className="mt-1.5 text-body-sm text-status-conflict-text" role="alert">
            {error}
          </p>
        )}
        {helperText && !error && (
          <p id={`${inputId}-helper`} className="mt-1.5 text-body-sm text-text-muted">
            {helperText}
          </p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'

export interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
  helperText?: string
  showCharCount?: boolean
  maxLength?: number
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, label, error, helperText, showCharCount, maxLength, id, ...props }, ref) => {
    const textareaId = id || label?.toLowerCase().replace(/\s+/g, '-')
    const value = (props.value || props.defaultValue || '') as string
    const charCount = value.length

    return (
      <div className="w-full">
        {label && (
          <label htmlFor={textareaId} className="block text-body-sm font-medium text-text-primary mb-1.5">
            {label}
          </label>
        )}
        <div className="relative">
          <textarea
            ref={ref}
            id={textareaId}
            className={cn(
              'w-full px-3.5 py-2.5 bg-canvas-elevated border rounded-control text-text-primary placeholder-text-muted resize-y min-h-[100px] font-sans',
              'transition-colors duration-fast',
              'focus:border-accent-DEFAULT focus:ring-2 focus:ring-accent-muted focus:outline-none',
              'disabled:bg-canvas-elevated/50 disabled:cursor-not-allowed',
              error
                ? 'border-status-conflict-border focus:border-status-conflict-DEFAULT focus:ring-status-conflict-muted'
                : 'border-border-DEFAULT hover:border-border-DEFAULT/80',
              className
            )}
            aria-invalid={error ? 'true' : 'false'}
            aria-describedby={error ? `${textareaId}-error` : helperText ? `${textareaId}-helper` : undefined}
            {...props}
          />
          {showCharCount && maxLength && (
            <div className="absolute bottom-2 right-2 text-meta text-text-muted">
              {charCount}/{maxLength}
            </div>
          )}
        </div>
        {error && (
          <p id={`${textareaId}-error`} className="mt-1.5 text-body-sm text-status-conflict-text" role="alert">
            {error}
          </p>
        )}
        {helperText && !error && (
          <p id={`${textareaId}-helper`} className="mt-1.5 text-body-sm text-text-muted">
            {helperText}
          </p>
        )}
      </div>
    )
  }
)

Textarea.displayName = 'Textarea'