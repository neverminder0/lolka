import { ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface SectionHeaderProps {
  /** Main heading text */
  title: string
  /** Optional subtitle text */
  subtitle?: string
  /** Optional description text */
  description?: string
  /** Additional content to render below description */
  children?: ReactNode
  /** Center align all content */
  centered?: boolean
  /** Custom className for container */
  className?: string
  /** Size variant */
  size?: 'sm' | 'md' | 'lg'
}

/**
 * Reusable section header component with consistent typography and spacing
 * 
 * @example
 * ```tsx
 * <SectionHeader
 *   title="Our Features"
 *   subtitle="Why Choose Us"
 *   description="Discover the powerful features that make us different"
 *   centered
 * />
 * ```
 */
export function SectionHeader({
  title,
  subtitle,
  description,
  children,
  centered = false,
  className,
  size = 'md'
}: SectionHeaderProps) {
  const sizeClasses = {
    sm: {
      title: 'text-2xl md:text-3xl',
      subtitle: 'text-sm',
      description: 'text-base',
      spacing: 'space-y-2'
    },
    md: {
      title: 'text-3xl md:text-4xl lg:text-5xl',
      subtitle: 'text-sm md:text-base',
      description: 'text-lg',
      spacing: 'space-y-4'
    },
    lg: {
      title: 'text-4xl md:text-5xl lg:text-6xl',
      subtitle: 'text-base md:text-lg',
      description: 'text-xl',
      spacing: 'space-y-6'
    }
  }

  const currentSize = sizeClasses[size]

  return (
    <div className={cn(
      currentSize.spacing,
      centered && 'text-center',
      'max-w-4xl',
      centered && 'mx-auto',
      className
    )}>
      {subtitle && (
        <p className={cn(
          'font-medium text-primary tracking-wider uppercase',
          currentSize.subtitle
        )}>
          {subtitle}
        </p>
      )}
      
      <h2 className={cn(
        'font-bold tracking-tight text-foreground',
        currentSize.title
      )}>
        {title}
      </h2>
      
      {description && (
        <p className={cn(
          'text-muted-foreground leading-relaxed',
          currentSize.description,
          centered ? 'max-w-2xl mx-auto' : 'max-w-3xl'
        )}>
          {description}
        </p>
      )}
      
      {children && (
        <div className="pt-2">
          {children}
        </div>
      )}
    </div>
  )
}