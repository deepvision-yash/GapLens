import type { Metadata } from 'next'
import { Plus_Jakarta_Sans, Roboto_Flex, Space_Mono } from 'next/font/google'
import '../globals.css'

const plusJakartaSans = Plus_Jakarta_Sans({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-plus-jakarta-sans',
  display: 'swap',
})

const robotoFlex = Roboto_Flex({
  subsets: ['latin'],
  weight: ['400', '500', '600'],
  variable: '--font-roboto-flex',
  display: 'swap',
})

const spaceMono = Space_Mono({
  subsets: ['latin'],
  weight: ['400', '700'],
  variable: '--font-space-mono',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'GapLens — AI Research Intelligence',
  description: 'See what\'s missing. Verify what matters.',
}

export default function LandingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${plusJakartaSans.variable} ${robotoFlex.variable} ${spaceMono.variable} dark`}>
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