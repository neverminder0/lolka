import { useState } from 'react'
import { motion } from 'framer-motion'
import { Check, X, Star, Zap, Crown, Rocket } from 'lucide-react'
import SectionHeader from '../components/SectionHeader'
import PricingCard from '../components/PricingCard'
import Button from '../components/Button'

const pricingPlans = {
  monthly: [
    {
      plan: 'Starter',
      price: '0',
      description: 'Perfect for getting started',
      icon: Zap,
      features: [
        { text: 'Up to 3 projects', included: true },
        { text: 'Basic components library', included: true },
        { text: 'Community support', included: true },
        { text: 'Basic analytics', included: true },
        { text: 'Standard themes', included: true },
        { text: 'Priority support', included: false },
        { text: 'Advanced components', included: false },
        { text: 'Custom integrations', included: false },
        { text: 'White-label options', included: false }
      ],
      buttonText: 'Get Started Free',
      buttonVariant: 'outline'
    },
    {
      plan: 'Professional',
      price: '29',
      description: 'Best for growing businesses',
      icon: Star,
      badge: 'Most Popular',
      highlighted: true,
      features: [
        { text: 'Unlimited projects', included: true },
        { text: 'Full components library', included: true },
        { text: 'Priority support', included: true },
        { text: 'Advanced analytics', included: true },
        { text: 'Premium themes', included: true },
        { text: 'API access', included: true },
        { text: 'Team collaboration', included: true },
        { text: 'Custom integrations', included: false },
        { text: 'White-label options', included: false }
      ],
      buttonText: 'Start Free Trial',
      buttonVariant: 'gradient'
    },
    {
      plan: 'Enterprise',
      price: '99',
      description: 'For large-scale applications',
      icon: Crown,
      features: [
        { text: 'Everything in Professional', included: true },
        { text: 'Dedicated support', included: true },
        { text: 'Custom integrations', included: true },
        { text: 'White-label options', included: true },
        { text: 'SSO authentication', included: true },
        { text: 'Advanced security', included: true },
        { text: 'Custom training', included: true },
        { text: 'SLA guarantee', included: true },
        { text: 'On-premise deployment', included: true }
      ],
      buttonText: 'Contact Sales',
      buttonVariant: 'outline'
    }
  ],
  yearly: [
    {
      plan: 'Starter',
      price: '0',
      description: 'Perfect for getting started',
      icon: Zap,
      features: [
        { text: 'Up to 3 projects', included: true },
        { text: 'Basic components library', included: true },
        { text: 'Community support', included: true },
        { text: 'Basic analytics', included: true },
        { text: 'Standard themes', included: true },
        { text: 'Priority support', included: false },
        { text: 'Advanced components', included: false },
        { text: 'Custom integrations', included: false },
        { text: 'White-label options', included: false }
      ],
      buttonText: 'Get Started Free',
      buttonVariant: 'outline'
    },
    {
      plan: 'Professional',
      price: '290',
      originalPrice: '348',
      description: 'Best for growing businesses',
      icon: Star,
      badge: 'Most Popular',
      highlighted: true,
      savings: '17% off',
      features: [
        { text: 'Unlimited projects', included: true },
        { text: 'Full components library', included: true },
        { text: 'Priority support', included: true },
        { text: 'Advanced analytics', included: true },
        { text: 'Premium themes', included: true },
        { text: 'API access', included: true },
        { text: 'Team collaboration', included: true },
        { text: 'Custom integrations', included: false },
        { text: 'White-label options', included: false }
      ],
      buttonText: 'Start Free Trial',
      buttonVariant: 'gradient'
    },
    {
      plan: 'Enterprise',
      price: '990',
      originalPrice: '1188',
      description: 'For large-scale applications',
      icon: Crown,
      savings: '17% off',
      features: [
        { text: 'Everything in Professional', included: true },
        { text: 'Dedicated support', included: true },
        { text: 'Custom integrations', included: true },
        { text: 'White-label options', included: true },
        { text: 'SSO authentication', included: true },
        { text: 'Advanced security', included: true },
        { text: 'Custom training', included: true },
        { text: 'SLA guarantee', included: true },
        { text: 'On-premise deployment', included: true }
      ],
      buttonText: 'Contact Sales',
      buttonVariant: 'outline'
    }
  ]
}

const faqs = [
  {
    question: 'Can I change plans at any time?',
    answer: 'Yes, you can upgrade or downgrade your plan at any time. Changes will be reflected in your next billing cycle.'
  },
  {
    question: 'Is there a free trial?',
    answer: 'Yes, we offer a 14-day free trial for all paid plans. No credit card required to get started.'
  },
  {
    question: 'What payment methods do you accept?',
    answer: 'We accept all major credit cards, PayPal, and bank transfers for enterprise customers.'
  },
  {
    question: 'Do you offer refunds?',
    answer: 'Yes, we offer a 30-day money-back guarantee. If you\'re not satisfied, contact us for a full refund.'
  },
  {
    question: 'Can I cancel my subscription?',
    answer: 'Yes, you can cancel your subscription at any time. You\'ll continue to have access until the end of your billing period.'
  },
  {
    question: 'Do you offer custom enterprise solutions?',
    answer: 'Yes, we offer custom solutions for enterprise customers including on-premise deployment and custom integrations.'
  }
]

const Pricing = () => {
  const [billingPeriod, setBillingPeriod] = useState('monthly')
  const [openFaq, setOpenFaq] = useState(null)

  const currentPlans = pricingPlans[billingPeriod]

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Hero Section */}
      <section className="section-padding bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
        <div className="container-custom">
          <SectionHeader
            badge="Pricing"
            title="Simple, transparent pricing"
            description="Choose the perfect plan for your needs. Start free and scale as you grow."
            className="mb-12"
          />

          {/* Billing Toggle */}
          <motion.div
            className="flex items-center justify-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="relative p-1 bg-gray-100 dark:bg-gray-800 rounded-2xl">
              <motion.div
                className="absolute top-1 left-1 w-24 h-10 bg-white dark:bg-gray-700 rounded-xl shadow-sm"
                animate={{
                  x: billingPeriod === 'monthly' ? 0 : 96
                }}
                transition={{ type: "spring", stiffness: 400, damping: 30 }}
              />
              <div className="relative flex">
                <button
                  onClick={() => setBillingPeriod('monthly')}
                  className={`px-6 py-2 text-sm font-medium rounded-xl transition-colors duration-200 ${
                    billingPeriod === 'monthly'
                      ? 'text-gray-900 dark:text-white'
                      : 'text-gray-600 dark:text-gray-400'
                  }`}
                >
                  Monthly
                </button>
                <button
                  onClick={() => setBillingPeriod('yearly')}
                  className={`px-6 py-2 text-sm font-medium rounded-xl transition-colors duration-200 flex items-center gap-2 ${
                    billingPeriod === 'yearly'
                      ? 'text-gray-900 dark:text-white'
                      : 'text-gray-600 dark:text-gray-400'
                  }`}
                >
                  Yearly
                  <span className="px-2 py-1 text-xs bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-full">
                    Save 17%
                  </span>
                </button>
              </div>
            </div>
          </motion.div>

          {/* Pricing Cards */}
          <div className="grid lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
            {currentPlans.map((plan, index) => (
              <motion.div
                key={`${plan.plan}-${billingPeriod}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 + index * 0.1 }}
              >
                <PricingCard
                  plan={plan.plan}
                  price={plan.price}
                  period={billingPeriod === 'yearly' ? '/year' : '/month'}
                  description={plan.description}
                  features={plan.features}
                  highlighted={plan.highlighted}
                  badge={plan.badge}
                  buttonText={plan.buttonText}
                  buttonVariant={plan.buttonVariant}
                  delay={index * 0.1}
                  className="h-full"
                />
                {plan.savings && (
                  <div className="text-center mt-4">
                    <span className="text-sm text-green-600 dark:text-green-400 font-medium">
                      {plan.savings} • Save ${plan.originalPrice - plan.price}
                    </span>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Comparison */}
      <section className="section-padding bg-white dark:bg-gray-900">
        <div className="container-custom">
          <SectionHeader
            title="Compare all features"
            description="See exactly what's included in each plan to make the best choice for your needs."
            className="mb-16"
          />

          <div className="overflow-x-auto">
            <motion.table
              className="w-full min-w-[800px] border-collapse"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="text-left py-4 px-6 font-semibold text-gray-900 dark:text-white">
                    Features
                  </th>
                  <th className="text-center py-4 px-6 font-semibold text-gray-900 dark:text-white">
                    Starter
                  </th>
                  <th className="text-center py-4 px-6 font-semibold text-gray-900 dark:text-white">
                    Professional
                  </th>
                  <th className="text-center py-4 px-6 font-semibold text-gray-900 dark:text-white">
                    Enterprise
                  </th>
                </tr>
              </thead>
              <tbody>
                {[
                  { feature: 'Projects', starter: '3', pro: 'Unlimited', enterprise: 'Unlimited' },
                  { feature: 'Components Library', starter: 'Basic', pro: 'Full', enterprise: 'Full + Custom' },
                  { feature: 'Support', starter: 'Community', pro: 'Priority', enterprise: 'Dedicated' },
                  { feature: 'Analytics', starter: 'Basic', pro: 'Advanced', enterprise: 'Advanced + Custom' },
                  { feature: 'Themes', starter: 'Standard', pro: 'Premium', enterprise: 'Premium + Custom' },
                  { feature: 'API Access', starter: false, pro: true, enterprise: true },
                  { feature: 'Team Collaboration', starter: false, pro: true, enterprise: true },
                  { feature: 'SSO Authentication', starter: false, pro: false, enterprise: true },
                  { feature: 'On-premise Deployment', starter: false, pro: false, enterprise: true }
                ].map((row, index) => (
                  <motion.tr
                    key={row.feature}
                    className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors duration-200"
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.4, delay: index * 0.05 }}
                  >
                    <td className="py-4 px-6 font-medium text-gray-900 dark:text-white">
                      {row.feature}
                    </td>
                    <td className="py-4 px-6 text-center text-gray-600 dark:text-gray-400">
                      {typeof row.starter === 'boolean' ? (
                        row.starter ? (
                          <Check className="w-5 h-5 text-green-500 mx-auto" />
                        ) : (
                          <X className="w-5 h-5 text-gray-400 mx-auto" />
                        )
                      ) : (
                        row.starter
                      )}
                    </td>
                    <td className="py-4 px-6 text-center text-gray-600 dark:text-gray-400">
                      {typeof row.pro === 'boolean' ? (
                        row.pro ? (
                          <Check className="w-5 h-5 text-green-500 mx-auto" />
                        ) : (
                          <X className="w-5 h-5 text-gray-400 mx-auto" />
                        )
                      ) : (
                        row.pro
                      )}
                    </td>
                    <td className="py-4 px-6 text-center text-gray-600 dark:text-gray-400">
                      {typeof row.enterprise === 'boolean' ? (
                        row.enterprise ? (
                          <Check className="w-5 h-5 text-green-500 mx-auto" />
                        ) : (
                          <X className="w-5 h-5 text-gray-400 mx-auto" />
                        )
                      ) : (
                        row.enterprise
                      )}
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </motion.table>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="section-padding bg-gray-50 dark:bg-gray-800">
        <div className="container-custom">
          <SectionHeader
            title="Frequently asked questions"
            description="Everything you need to know about our pricing and plans."
            className="mb-16"
          />

          <div className="max-w-3xl mx-auto">
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                className="mb-4"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <button
                  onClick={() => setOpenFaq(openFaq === index ? null : index)}
                  className="w-full p-6 text-left glass-effect rounded-2xl hover:shadow-lg transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-primary-500/50"
                >
                  <div className="flex justify-between items-center">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      {faq.question}
                    </h3>
                    <motion.div
                      animate={{ rotate: openFaq === index ? 45 : 0 }}
                      transition={{ duration: 0.2 }}
                      className="text-primary-600 dark:text-primary-400"
                    >
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                    </motion.div>
                  </div>
                  <motion.div
                    initial={false}
                    animate={{
                      height: openFaq === index ? 'auto' : 0,
                      opacity: openFaq === index ? 1 : 0
                    }}
                    transition={{ duration: 0.3 }}
                    className="overflow-hidden"
                  >
                    <p className="mt-4 text-gray-600 dark:text-gray-400 leading-relaxed">
                      {faq.answer}
                    </p>
                  </motion.div>
                </button>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-gradient-to-r from-primary-600 to-secondary-400">
        <div className="container-custom text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="max-w-3xl mx-auto"
          >
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-6">
              Ready to get started?
            </h2>
            <p className="text-xl text-white/90 mb-8 leading-relaxed">
              Join thousands of developers and start building amazing experiences today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="outline" size="xl" className="bg-white text-primary-600 border-white hover:bg-gray-50">
                Start Free Trial
              </Button>
              <Button variant="ghost" size="xl" className="text-white border-white/30 hover:bg-white/10">
                Contact Sales
              </Button>
            </div>
          </motion.div>
        </div>
      </section>
    </motion.div>
  )
}

export default Pricing