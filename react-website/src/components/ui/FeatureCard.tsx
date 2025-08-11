import { } from 'react'
import { LucideIcon } from 'lucide-react'
import { motion } from 'framer-motion'
import { Badge } from './Badge'
import { cn } from '@/lib/utils'

interface FeatureCardProps {
  /** Icon component from lucide-react */
  icon: LucideIcon
  /** Feature title */
  title: string
  /** Feature description */
  description: string
  /** Optional list of feature highlights */
  features?: string[]
  /** Optional badge text */
  badge?: string
  /** Optional premium badge */
  isPremium?: boolean
  /** Animation delay for staggered animations */
  delay?: number
  /** Custom className */
  className?: string
}

/**
 * Feature card component with icon, title, description, and optional features list
 * 
 * @example
 * ```tsx
 * <FeatureCard
 *   icon={Zap}
 *   title="Lightning Fast"
 *   description="Built for speed with modern optimization techniques"
 *   features={["Hot reload", "Optimized builds", "Tree shaking"]}
 *   badge="Popular"
 * />
 * ```
 */
export function FeatureCard({
  icon: Icon,
  title,
  description,
  features,
  badge,
  isPremium = false,
  delay = 0,
  className
}: FeatureCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay }}
      className={cn(
        'group relative p-6 rounded-2xl glass hover:glass-strong transition-all duration-300 hover:scale-105 hover:shadow-lg',
        isPremium && 'ring-2 ring-primary/20',
        className
      )}
    >
      {/* Badge */}
      {badge && (
        <div className="absolute -top-2 -right-2">
          <Badge variant={isPremium ? 'gradient' : 'secondary'}>
            {badge}
          </Badge>
        </div>
      )}

      <div className="space-y-4">
        {/* Icon */}
        <div className={cn(
          'p-3 rounded-xl w-fit transition-all duration-300',
          isPremium 
            ? 'bg-gradient-primary text-white group-hover:shadow-lg group-hover:shadow-primary/25' 
            : 'bg-primary/10 text-primary group-hover:bg-primary/20'
        )}>
          <Icon className="h-6 w-6" />
        </div>

        {/* Content */}
        <div className="space-y-2">
          <h3 className="text-xl font-semibold text-foreground group-hover:text-primary transition-colors">
            {title}
          </h3>
          <p className="text-muted-foreground leading-relaxed">
            {description}
          </p>
        </div>

        {/* Features List */}
        {features && features.length > 0 && (
          <ul className="space-y-2 pt-2">
            {features.map((feature, index) => (
              <li key={index} className="flex items-center text-sm">
                <div className="h-1.5 w-1.5 rounded-full bg-primary mr-3 flex-shrink-0" />
                <span className="text-muted-foreground">{feature}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </motion.div>
  )
}