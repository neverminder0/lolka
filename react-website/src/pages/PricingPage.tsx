import { useState } from 'react'
import { motion } from 'framer-motion'
import { Check, Star, Shield, Zap } from 'lucide-react'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { PricingCard } from '@/components/ui/PricingCard'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { cn } from '@/lib/utils'

const plans = [
  {
    name: 'Starter',
    description: 'Perfect for individuals and small projects',
    monthlyPrice: 0,
    yearlyPrice: 0,
    features: [
      '1 team member',
      '3 projects',
      '5GB storage',
      'Community support',
      'Basic templates',
      'SSL certificate'
    ],
    excludedFeatures: [
      'Advanced integrations',
      'Custom domains',
      'Priority support'
    ]
  },
  {
    name: 'Pro',
    description: 'Ideal for growing teams and businesses',
    monthlyPrice: 29,
    yearlyPrice: 290,
    isPopular: true,
    features: [
      '10 team members',
      'Unlimited projects',
      '100GB storage',
      'Priority support',
      'Advanced templates',
      'Custom domains',
      'Advanced integrations',
      'Team collaboration',
      'Version control',
      'Analytics dashboard'
    ]
  },
  {
    name: 'Enterprise',
    description: 'For large organizations with advanced needs',
    monthlyPrice: 99,
    yearlyPrice: 990,
    isPremium: true,
    features: [
      'Unlimited team members',
      'Unlimited projects',
      '1TB storage',
      '24/7 premium support',
      'All templates & themes',
      'White-label solution',
      'Advanced security',
      'SSO integration',
      'Custom integrations',
      'Dedicated account manager',
      'SLA guarantees',
      'Advanced analytics'
    ]
  }
]

const faqs = [
  {
    question: 'Can I change my plan at any time?',
    answer: 'Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately, and we\'ll prorate any billing differences.'
  },
  {
    question: 'Is there a free trial available?',
    answer: 'Yes! All paid plans come with a 14-day free trial. No credit card required to start your trial.'
  },
  {
    question: 'What payment methods do you accept?',
    answer: 'We accept all major credit cards (Visa, MasterCard, American Express) and PayPal. Enterprise customers can also pay by invoice.'
  },
  {
    question: 'Can I cancel my subscription?',
    answer: 'You can cancel your subscription at any time. Your account will remain active until the end of your current billing period.'
  },
  {
    question: 'Do you offer refunds?',
    answer: 'We offer a 30-day money-back guarantee for all paid plans. If you\'re not satisfied, we\'ll provide a full refund.'
  },
  {
    question: 'Is my data secure?',
    answer: 'Absolutely. We use enterprise-grade security measures including SSL encryption, regular backups, and SOC 2 compliance.'
  }
]

/**
 * Comprehensive Pricing page with plan comparison and FAQ
 */
export default function PricingPage() {
  const [isYearly, setIsYearly] = useState(false)

  const handlePlanSelect = (planName: string) => {
    // Handle plan selection logic here
    console.log(`Selected plan: ${planName}`)
  }

  return (
    <div className="min-h-screen pt-24">
      {/* Hero Section */}
      <section className="py-16">
        <div className="container-grid">
          <div className="col-span-12 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-6"
            >
              <Badge variant="gradient" className="mb-4">
                💰 Simple Pricing
              </Badge>
              
              <SectionHeader
                title="Choose Your Perfect Plan"
                subtitle="Pricing That Scales"
                description="Start free and scale as you grow. All plans include our core features with increasing limits and premium support."
                centered
                size="lg"
              />
            </motion.div>
          </div>
        </div>
      </section>

      {/* Billing Toggle */}
      <section className="pb-16">
        <div className="container-grid">
          <div className="col-span-12 flex justify-center">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex items-center space-x-4 glass p-2 rounded-2xl"
            >
              <span className={cn(
                'text-sm font-medium transition-colors',
                !isYearly ? 'text-foreground' : 'text-muted-foreground'
              )}>
                Monthly
              </span>
              
              <button
                onClick={() => setIsYearly(!isYearly)}
                className={cn(
                  'relative inline-flex items-center h-6 w-11 rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
                  isYearly ? 'bg-primary' : 'bg-muted'
                )}
                role="switch"
                aria-checked={isYearly}
                aria-label="Toggle yearly billing"
              >
                <span
                  className={cn(
                    'inline-block h-4 w-4 rounded-full bg-white transition-transform',
                    isYearly ? 'translate-x-6' : 'translate-x-1'
                  )}
                />
              </button>
              
              <div className="flex items-center space-x-2">
                <span className={cn(
                  'text-sm font-medium transition-colors',
                  isYearly ? 'text-foreground' : 'text-muted-foreground'
                )}>
                  Yearly
                </span>
                <Badge variant="success" className="text-xs">
                  Save 20%
                </Badge>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Pricing Plans */}
      <section className="pb-24">
        <div className="container-grid">
          <div className="col-span-12">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {plans.map((plan, index) => (
                <PricingCard
                  key={plan.name}
                  {...plan}
                  isYearly={isYearly}
                  delay={index * 0.1}
                  onSelectPlan={() => handlePlanSelect(plan.name)}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Comparison */}
      <section className="py-24 bg-muted/30">
        <div className="container-grid">
          <div className="col-span-12">
            <SectionHeader
              title="Compare All Features"
              subtitle="Feature Comparison"
              description="See exactly what's included in each plan to make the best choice for your needs."
              centered
              className="mb-16"
            />
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-4 px-6 font-semibold">Features</th>
                    <th className="text-center py-4 px-6 font-semibold">Starter</th>
                    <th className="text-center py-4 px-6 font-semibold">
                      <div className="flex items-center justify-center space-x-2">
                        <span>Pro</span>
                        <Badge variant="gradient" className="text-xs">Popular</Badge>
                      </div>
                    </th>
                    <th className="text-center py-4 px-6 font-semibold">Enterprise</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { feature: 'Team Members', starter: '1', pro: '10', enterprise: 'Unlimited' },
                    { feature: 'Projects', starter: '3', pro: 'Unlimited', enterprise: 'Unlimited' },
                    { feature: 'Storage', starter: '5GB', pro: '100GB', enterprise: '1TB' },
                    { feature: 'Support', starter: 'Community', pro: 'Priority', enterprise: '24/7 Premium' },
                    { feature: 'Custom Domain', starter: false, pro: true, enterprise: true },
                    { feature: 'Advanced Analytics', starter: false, pro: true, enterprise: true },
                    { feature: 'SSO Integration', starter: false, pro: false, enterprise: true },
                    { feature: 'White-label', starter: false, pro: false, enterprise: true }
                  ].map((row, index) => (
                    <tr key={index} className="border-b border-border/50">
                      <td className="py-4 px-6 font-medium">{row.feature}</td>
                      <td className="py-4 px-6 text-center">
                        {typeof row.starter === 'boolean' ? (
                          row.starter ? <Check className="h-5 w-5 text-green-500 mx-auto" /> : <span className="text-muted-foreground">-</span>
                        ) : (
                          row.starter
                        )}
                      </td>
                      <td className="py-4 px-6 text-center">
                        {typeof row.pro === 'boolean' ? (
                          row.pro ? <Check className="h-5 w-5 text-green-500 mx-auto" /> : <span className="text-muted-foreground">-</span>
                        ) : (
                          row.pro
                        )}
                      </td>
                      <td className="py-4 px-6 text-center">
                        {typeof row.enterprise === 'boolean' ? (
                          row.enterprise ? <Check className="h-5 w-5 text-green-500 mx-auto" /> : <span className="text-muted-foreground">-</span>
                        ) : (
                          row.enterprise
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-24">
        <div className="container-grid">
          <div className="col-span-12 lg:col-span-8 lg:col-start-3">
            <SectionHeader
              title="Frequently Asked Questions"
              subtitle="FAQ"
              description="Have questions? We have answers. If you can't find what you're looking for, feel free to contact our support team."
              centered
              className="mb-16"
            />
            
            <div className="space-y-8">
              {faqs.map((faq, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="glass p-6 rounded-2xl"
                >
                  <h3 className="text-lg font-semibold text-foreground mb-3">
                    {faq.question}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {faq.answer}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-mesh">
        <div className="container-grid">
          <div className="col-span-12 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-8"
            >
              <div className="space-y-4">
                <h2 className="text-3xl md:text-5xl font-bold tracking-tight text-white">
                  Ready to Get Started?
                </h2>
                <p className="text-xl text-white/80 max-w-2xl mx-auto">
                  Join thousands of developers and teams who trust our platform for their projects.
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button variant="secondary" size="xl">
                  Start Free Trial
                </Button>
                <Button variant="outline" size="xl" className="bg-white/10 border-white/20 text-white hover:bg-white/20">
                  Contact Sales
                </Button>
              </div>
              
              <p className="text-sm text-white/60">
                No credit card required • 14-day free trial • Cancel anytime
              </p>
            </motion.div>
          </div>
        </div>
      </section>
    </div>
  )
}