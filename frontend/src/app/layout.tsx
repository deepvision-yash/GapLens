import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'GapLens — AI Research Intelligence',
  description: 'See what\'s missing. Verify what matters.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet" />
      </head>
      <body className="min-h-screen bg-background text-on-surface antialiased overscroll-none">
        {children}
      </body>
    </html>
  )
}