import { motion } from 'framer-motion'
import { Check, X } from 'lucide-react'
import Button from './Button'
import Badge from './Badge'

const PricingCard = ({ 
  plan, 
  price, 
  period = '/month', 
  description, 
  features, 
  highlighted = false,
  badge,
  buttonText = 'Get Started',
  buttonVariant = 'primary',
  delay = 0,
  ...props 
}) => {
  return (
    <motion.div
      className={`relative p-8 rounded-2xl transition-all duration-300 ${
        highlighted 
          ? 'glass-effect shadow-glow ring-2 ring-primary-500/20 scale-105' 
          : 'glass-effect hover:shadow-glow'
      }`}
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.6, delay, ease: "easeOut" }}
      whileHover={{ y: highlighted ? 0 : -5 }}
      {...props}
    >
      {badge && (
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
          <Badge variant="gradient" size="md">
            {badge}
          </Badge>
        </div>
      )}

      <div className="text-center mb-8">
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          {plan}
        </h3>
        <p className="text-gray-600 dark:text-gray-400 mb-4">
          {description}
        </p>
        <div className="flex items-baseline justify-center gap-1">
          <span className="text-4xl font-bold text-gradient">
            ${price}
          </span>
          <span className="text-gray-600 dark:text-gray-400">
            {period}
          </span>
        </div>
      </div>

      <div className="space-y-4 mb-8">
        {features.map((feature, index) => (
          <motion.div
            key={index}
            className="flex items-center gap-3"
            initial={{ opacity: 0, x: -10 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, delay: delay + 0.1 + index * 0.05 }}
          >
            {feature.included ? (
              <div className="flex-shrink-0 w-5 h-5 rounded-full bg-green-500 flex items-center justify-center">
                <Check className="w-3 h-3 text-white" />
              </div>
            ) : (
              <div className="flex-shrink-0 w-5 h-5 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center">
                <X className="w-3 h-3 text-gray-500" />
              </div>
            )}
            <span className={`text-sm ${
              feature.included 
                ? 'text-gray-900 dark:text-white' 
                : 'text-gray-500 dark:text-gray-400 line-through'
            }`}>
              {feature.text}
            </span>
          </motion.div>
        ))}
      </div>

      <Button 
        variant={highlighted ? 'gradient' : buttonVariant} 
        size="lg" 
        className="w-full"
      >
        {buttonText}
      </Button>
    </motion.div>
  )
}

export default PricingCard

// Example usage:
// <PricingCard
//   plan="Pro"
//   price="29"
//   description="Perfect for growing businesses"
//   badge="Most Popular"
//   highlighted={true}
//   features={[
//     { text: "Unlimited projects", included: true },
//     { text: "Priority support", included: true },
//     { text: "Advanced analytics", included: false }
//   ]}
//   delay={0.1}
// />