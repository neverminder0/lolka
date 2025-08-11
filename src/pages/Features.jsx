import { motion } from 'framer-motion'
import { 
  Zap, 
  Shield, 
  Palette, 
  Smartphone, 
  Globe, 
  Rocket,
  Code,
  Users,
  BarChart,
  Settings,
  Lock,
  Layers
} from 'lucide-react'
import SectionHeader from '../components/SectionHeader'
import FeatureCard from '../components/FeatureCard'

const mainFeatures = [
  {
    icon: Zap,
    title: 'Lightning Fast Performance',
    description: 'Optimized with modern build tools, lazy loading, and code splitting for blazing fast load times under 2 seconds.',
    details: [
      'Vite build system for instant hot reload',
      'Tree-shaking and dead code elimination',
      'Image optimization and lazy loading',
      'Critical CSS inlining'
    ]
  },
  {
    icon: Shield,
    title: 'Enterprise Security',
    description: 'Built with security-first principles, featuring data encryption, secure authentication, and compliance standards.',
    details: [
      'End-to-end encryption',
      'OAuth 2.0 and SSO integration',
      'GDPR and SOC 2 compliance',
      'Regular security audits'
    ]
  },
  {
    icon: Palette,
    title: 'Beautiful Design System',
    description: 'Comprehensive design system with glassmorphism effects, smooth animations, and consistent styling.',
    details: [
      'Tailwind CSS with custom theme',
      'Framer Motion animations',
      'Dark/Light mode support',
      'Accessible color schemes'
    ]
  }
]

const additionalFeatures = [
  {
    icon: Smartphone,
    title: 'Mobile-First Design',
    description: 'Responsive layouts that look perfect on all devices with touch-optimized interactions.'
  },
  {
    icon: Globe,
    title: 'Internationalization',
    description: 'Built-in i18n support with RTL languages and localization management.'
  },
  {
    icon: Code,
    title: 'Developer Experience',
    description: 'TypeScript support, ESLint, Prettier, and comprehensive documentation.'
  },
  {
    icon: Users,
    title: 'Team Collaboration',
    description: 'Real-time collaboration tools with comments, reviews, and version control.'
  },
  {
    icon: BarChart,
    title: 'Advanced Analytics',
    description: 'Detailed insights with custom dashboards and real-time data visualization.'
  },
  {
    icon: Settings,
    title: 'Customizable',
    description: 'Highly configurable with theming, plugins, and extension system.'
  }
]

const integrations = [
  { name: 'React', logo: '⚛️' },
  { name: 'TypeScript', logo: '🔷' },
  { name: 'Tailwind CSS', logo: '🎨' },
  { name: 'Framer Motion', logo: '🎭' },
  { name: 'Vite', logo: '⚡' },
  { name: 'ESLint', logo: '🔍' },
  { name: 'Prettier', logo: '💅' },
  { name: 'GitHub', logo: '🐙' },
  { name: 'Vercel', logo: '▲' },
  { name: 'Netlify', logo: '🌐' },
  { name: 'Firebase', logo: '🔥' },
  { name: 'Supabase', logo: '⚡' }
]

const Features = () => {
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
            badge="Features"
            title="Everything you need to build amazing experiences"
            description="Discover our comprehensive suite of features designed to help you create stunning, fast, and secure web applications."
            className="mb-16"
          />

          {/* Main Features Grid */}
          <div className="grid lg:grid-cols-3 gap-8 mb-16">
            {mainFeatures.map((feature, index) => (
              <motion.div
                key={feature.title}
                className="p-8 glass-effect rounded-2xl hover:shadow-glow transition-all duration-300"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                <div className="flex items-center justify-center w-16 h-16 mb-6 rounded-2xl bg-gradient-to-r from-primary-600 to-secondary-400">
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 dark:text-gray-400 mb-6 leading-relaxed">
                  {feature.description}
                </p>

                <ul className="space-y-2">
                  {feature.details.map((detail, detailIndex) => (
                    <motion.li
                      key={detailIndex}
                      className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400"
                      initial={{ opacity: 0, x: -10 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ duration: 0.4, delay: index * 0.1 + detailIndex * 0.05 }}
                    >
                      <div className="w-1.5 h-1.5 rounded-full bg-primary-500" />
                      {detail}
                    </motion.li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Additional Features */}
      <section className="section-padding bg-white dark:bg-gray-900">
        <div className="container-custom">
          <SectionHeader
            title="Powerful capabilities for modern development"
            description="Explore additional features that make development faster, easier, and more enjoyable."
            className="mb-16"
          />

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {additionalFeatures.map((feature, index) => (
              <FeatureCard
                key={feature.title}
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
                delay={index * 0.1}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Integrations Section */}
      <section className="section-padding bg-gray-50 dark:bg-gray-800">
        <div className="container-custom">
          <SectionHeader
            title="Seamless integrations"
            description="Works perfectly with your favorite tools and services out of the box."
            className="mb-16"
          />

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6">
            {integrations.map((integration, index) => (
              <motion.div
                key={integration.name}
                className="p-6 glass-effect rounded-2xl text-center hover:shadow-lg transition-all duration-300 group"
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ duration: 0.5, delay: index * 0.05 }}
                whileHover={{ y: -5 }}
              >
                <div className="text-3xl mb-3 group-hover:scale-110 transition-transform duration-300">
                  {integration.logo}
                </div>
                <div className="text-sm font-medium text-gray-900 dark:text-white">
                  {integration.name}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Detailed Feature Showcase */}
      <section className="section-padding bg-white dark:bg-gray-900">
        <div className="container-custom">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            {/* Content */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <div className="mb-6">
                <div className="inline-flex items-center justify-center w-12 h-12 mb-4 rounded-xl bg-gradient-to-r from-primary-600 to-secondary-400">
                  <Layers className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                  Component-driven architecture
                </h3>
                <p className="text-lg text-gray-600 dark:text-gray-400 leading-relaxed">
                  Build with confidence using our modular, reusable component system. 
                  Each component is carefully crafted with accessibility, performance, 
                  and customization in mind.
                </p>
              </div>

              <div className="space-y-4">
                {[
                  'Fully typed with TypeScript',
                  'Comprehensive prop interfaces',
                  'Built-in accessibility features',
                  'Consistent design tokens',
                  'Extensive documentation'
                ].map((item, index) => (
                  <motion.div
                    key={index}
                    className="flex items-center gap-3"
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: 0.1 + index * 0.1 }}
                  >
                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-500 flex items-center justify-center">
                      <div className="w-2 h-2 rounded-full bg-white" />
                    </div>
                    <span className="text-gray-700 dark:text-gray-300">
                      {item}
                    </span>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            {/* Visual */}
            <motion.div
              className="relative"
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              <div className="relative p-8 glass-effect rounded-2xl shadow-glow">
                <div className="grid grid-cols-2 gap-4">
                  {[1, 2, 3, 4].map((item) => (
                    <motion.div
                      key={item}
                      className="aspect-square rounded-xl bg-gradient-to-br from-primary-400/20 to-secondary-400/20 flex items-center justify-center"
                      whileHover={{ scale: 1.05 }}
                      transition={{ type: "spring", stiffness: 400, damping: 17 }}
                    >
                      <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-primary-500 to-secondary-500" />
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Floating Elements */}
              <motion.div
                className="absolute -top-4 -right-4 w-8 h-8 bg-primary-500 rounded-full"
                animate={{ 
                  y: [0, -10, 0],
                  scale: [1, 1.1, 1]
                }}
                transition={{ 
                  duration: 2, 
                  repeat: Infinity,
                  ease: "easeInOut" 
                }}
              />
              <motion.div
                className="absolute -bottom-4 -left-4 w-6 h-6 bg-secondary-400 rounded-full"
                animate={{ 
                  y: [0, 10, 0],
                  scale: [1, 1.2, 1]
                }}
                transition={{ 
                  duration: 3, 
                  repeat: Infinity,
                  ease: "easeInOut",
                  delay: 1 
                }}
              />
            </motion.div>
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
              Ready to experience the difference?
            </h2>
            <p className="text-xl text-white/90 mb-8 leading-relaxed">
              Start building with our feature-rich platform today and see why developers love our tools.
            </p>
            <motion.button
              className="px-8 py-4 bg-white text-primary-600 rounded-2xl font-semibold text-lg hover:bg-gray-50 transition-colors duration-200 shadow-lg"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Start Free Trial
            </motion.button>
          </motion.div>
        </div>
      </section>
    </motion.div>
  )
}

export default Features