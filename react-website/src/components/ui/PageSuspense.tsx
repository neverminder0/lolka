import { Suspense, ReactNode } from 'react'
import { Loader2 } from 'lucide-react'

interface PageSuspenseProps {
  children: ReactNode
}

/**
 * Loading fallback component for Suspense
 */
function PageLoader() {
  return (
    <div className="flex items-center justify-center min-h-[50vh]">
      <div className="flex flex-col items-center space-y-4">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <p className="text-sm text-muted-foreground">Loading...</p>
      </div>
    </div>
  )
}

/**
 * Suspense wrapper for page components with loading fallback
 */
export function PageSuspense({ children }: PageSuspenseProps) {
  return (
    <Suspense fallback={<PageLoader />}>
      {children}
    </Suspense>
  )
}