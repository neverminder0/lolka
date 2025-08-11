import { } from 'react'
import { Check, X } from 'lucide-react'
import { motion } from 'framer-motion'
import { Button } from './Button'
import { Badge } from './Badge'
import { cn } from '@/lib/utils'

interface PricingCardProps {
  /** Plan name */
  name: string
  /** Plan description */
  description: string
  /** Monthly price */
  monthlyPrice: number
  /** Yearly price */
  yearlyPrice: number
  /** Whether yearly billing is selected */
  isYearly: boolean
  /** List of included features */
  features: string[]
  /** List of excluded features (optional) */
  excludedFeatures?: string[]
  /** Whether this is the most popular plan */
  isPopular?: boolean
  /** Whether this is a premium/enterprise plan */
  isPremium?: boolean
  /** Call-to-action button text */
  ctaText?: string
  /** Custom className */
  className?: string
  /** Animation delay */
  delay?: number
  /** Click handler for CTA button */
  onSelectPlan?: () => void
}

/**
 * Pricing card component with features, pricing toggle, and CTA
 * 
 * @example
 * ```tsx
 * <PricingCard
 *   name="Pro"
 *   description="Perfect for growing teams"
 *   monthlyPrice={29}
 *   yearlyPrice={290}
 *   isYearly={true}
 *   features={["10 team members", "Unlimited projects", "24/7 support"]}
 *   isPopular
 * />
 * ```
 */
export function PricingCard({
  name,
  description,
  monthlyPrice,
  yearlyPrice,
  isYearly,
  features,
  excludedFeatures = [],
  isPopular = false,
  isPremium = false,
  ctaText,
  className,
  delay = 0,
  onSelectPlan
}: PricingCardProps) {
  const currentPrice = isYearly ? yearlyPrice : monthlyPrice
  const savings = isYearly ? Math.round(((monthlyPrice * 12 - yearlyPrice) / (monthlyPrice * 12)) * 100) : 0
  
  const defaultCtaText = () => {
    if (monthlyPrice === 0) return 'Get Started Free'
    if (isPremium) return 'Contact Sales'
    return 'Start Free Trial'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay }}
      className={cn(
        'relative p-8 rounded-3xl transition-all duration-300 hover:scale-105',
        isPopular && 'ring-2 ring-primary scale-105',
        isPremium 
          ? 'bg-gradient-mesh text-white' 
          : 'glass hover:glass-strong',
        className
      )}
    >
      {/* Popular Badge */}
      {isPopular && (
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
          <Badge variant="gradient" className="px-4 py-1">
            Most Popular
          </Badge>
        </div>
      )}

      <div className="space-y-6">
        {/* Header */}
        <div className="space-y-2">
          <h3 className={cn(
            'text-2xl font-bold',
            isPremium ? 'text-white' : 'text-foreground'
          )}>
            {name}
          </h3>
          <p className={cn(
            'text-sm',
            isPremium ? 'text-white/80' : 'text-muted-foreground'
          )}>
            {description}
          </p>
        </div>

        {/* Pricing */}
        <div className="space-y-2">
          <div className="flex items-baseline space-x-2">
            <span className={cn(
              'text-4xl font-bold',
              isPremium ? 'text-white' : 'text-foreground'
            )}>
              {currentPrice === 0 ? 'Free' : `$${currentPrice}`}
            </span>
            {currentPrice > 0 && (
              <span className={cn(
                'text-sm',
                isPremium ? 'text-white/60' : 'text-muted-foreground'
              )}>
                /{isYearly ? 'year' : 'month'}
              </span>
            )}
          </div>
          
          {/* Savings indicator */}
          {isYearly && savings > 0 && currentPrice > 0 && (
            <div className="text-sm text-green-500 font-medium">
              Save {savings}% with yearly billing
            </div>
          )}
          
          {/* Monthly equivalent for yearly plans */}
          {isYearly && currentPrice > 0 && (
            <div className={cn(
              'text-sm',
              isPremium ? 'text-white/60' : 'text-muted-foreground'
            )}>
              ${Math.round(currentPrice / 12)}/month billed annually
            </div>
          )}
        </div>

        {/* CTA Button */}
        <Button
          variant={isPopular ? 'gradient' : isPremium ? 'secondary' : 'default'}
          size="lg"
          className="w-full"
          onClick={onSelectPlan}
        >
          {ctaText || defaultCtaText()}
        </Button>

        {/* Features */}
        <div className="space-y-4">
          <h4 className={cn(
            'font-semibold',
            isPremium ? 'text-white' : 'text-foreground'
          )}>
            What's included:
          </h4>
          
          <ul className="space-y-3">
            {features.map((feature, index) => (
              <li key={index} className="flex items-start space-x-3">
                <Check className={cn(
                  'h-5 w-5 flex-shrink-0 mt-0.5',
                  isPremium ? 'text-green-400' : 'text-green-500'
                )} />
                <span className={cn(
                  'text-sm',
                  isPremium ? 'text-white/90' : 'text-foreground'
                )}>
                  {feature}
                </span>
              </li>
            ))}
          </ul>

          {/* Excluded features */}
          {excludedFeatures.length > 0 && (
            <ul className="space-y-3 pt-4 border-t border-border/20">
              {excludedFeatures.map((feature, index) => (
                <li key={index} className="flex items-start space-x-3">
                  <X className={cn(
                    'h-5 w-5 flex-shrink-0 mt-0.5',
                    isPremium ? 'text-red-400' : 'text-red-500'
                  )} />
                  <span className={cn(
                    'text-sm opacity-60',
                    isPremium ? 'text-white/60' : 'text-muted-foreground'
                  )}>
                    {feature}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </motion.div>
  )
}