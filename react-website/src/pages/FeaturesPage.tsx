import { motion } from 'framer-motion'
import {
  Zap, Shield, Users, Rocket, Code, Smartphone, Globe, BarChart,
  Lock, Cpu, Database, Cloud, Bell
} from 'lucide-react'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { FeatureCard } from '@/components/ui/FeatureCard'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { Link } from 'react-router-dom'

const coreFeatures = [
  {
    icon: Zap,
    title: 'Lightning Fast Performance',
    description: 'Optimized for speed with modern build tools and performance techniques.',
    features: ['Hot module replacement', 'Tree shaking', 'Code splitting', 'Bundle optimization'],
    badge: 'Popular'
  },
  {
    icon: Shield,
    title: 'Enterprise Security',
    description: 'Built-in security features to protect your applications and data.',
    features: ['End-to-end encryption', 'RBAC permissions', 'Audit logging', 'Compliance ready'],
    isPremium: true,
    badge: 'Pro'
  },
  {
    icon: Users,
    title: 'Team Collaboration',
    description: 'Work together seamlessly with real-time collaboration features.',
    features: ['Real-time editing', 'Comments & reviews', 'Version control', 'Team workspaces']
  },
  {
    icon: Rocket,
    title: 'Easy Deployment',
    description: 'Deploy anywhere with our simple one-click deployment solutions.',
    features: ['One-click deploy', 'Multiple providers', 'Auto scaling', 'CDN integration']
  }
]

const developerFeatures = [
  {
    icon: Code,
    title: 'Developer Experience',
    description: 'Tools and features designed to enhance developer productivity.',
    features: ['IntelliSense support', 'Debugging tools', 'Error tracking', 'Performance monitoring']
  },
  {
    icon: Smartphone,
    title: 'Mobile First',
    description: 'Responsive design that works perfectly on all device sizes.',
    features: ['Touch optimized', 'Offline support', 'PWA ready', 'App store deployment']
  },
  {
    icon: Globe,
    title: 'Global CDN',
    description: 'Deliver content at lightning speed with our global edge network.',
    features: ['99.9% uptime SLA', '150+ edge locations', 'Smart routing', 'DDoS protection']
  },
  {
    icon: BarChart,
    title: 'Advanced Analytics',
    description: 'Comprehensive insights into your application performance and usage.',
    features: ['Real-time metrics', 'Custom dashboards', 'Alerts & notifications', 'Export reports']
  }
]

const integrationFeatures = [
  {
    icon: Database,
    title: 'Database Integration',
    description: 'Connect to any database with our flexible data layer.',
    features: ['PostgreSQL', 'MongoDB', 'Redis', 'GraphQL APIs']
  },
  {
    icon: Cloud,
    title: 'Cloud Native',
    description: 'Built for the cloud with containerization and orchestration support.',
    features: ['Docker support', 'Kubernetes ready', 'Auto-scaling', 'Health checks']
  },
  {
    icon: Lock,
    title: 'Authentication',
    description: 'Secure user authentication with multiple provider support.',
    features: ['OAuth 2.0', 'SAML SSO', 'Multi-factor auth', 'Social logins']
  },
  {
    icon: Bell,
    title: 'Notifications',
    description: 'Keep users engaged with powerful notification systems.',
    features: ['Push notifications', 'Email campaigns', 'In-app messages', 'SMS alerts']
  }
]

/**
 * Comprehensive Features page showcasing all platform capabilities
 */
export default function FeaturesPage() {
  return (
    <div className="min-h-screen pt-24">
      {/* Hero Section */}
      <section className="py-16 bg-gradient-mesh">
        <div className="container-grid">
          <div className="col-span-12 lg:col-span-8 lg:col-start-3 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-6"
            >
              <Badge variant="gradient" className="mb-4">
                ✨ Powerful Features
              </Badge>
              
              <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-white">
                Everything You Need to{' '}
                <span className="text-secondary">Build Amazing Apps</span>
              </h1>
              
              <p className="text-xl text-white/80 max-w-2xl mx-auto">
                Discover the comprehensive set of features that make development faster, 
                more secure, and incredibly enjoyable.
              </p>
              
              <Button variant="secondary" size="lg" asChild>
                <Link to="/pricing">Start Building Today</Link>
              </Button>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Core Features */}
      <section className="py-24">
        <div className="container-grid">
          <div className="col-span-12">
            <SectionHeader
              subtitle="Core Features"
              title="Built for Modern Development"
              description="Essential features that power your development workflow and deliver exceptional user experiences."
              centered
              className="mb-16"
            />
          </div>
          
          <div className="col-span-12">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {coreFeatures.map((feature, index) => (
                <FeatureCard
                  key={feature.title}
                  {...feature}
                  delay={index * 0.1}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Developer Features */}
      <section className="py-24 bg-muted/30">
        <div className="container-grid">
          <div className="col-span-12">
            <SectionHeader
              subtitle="Developer Tools"
              title="Enhanced Developer Experience"
              description="Powerful tools and features designed to boost productivity and streamline your development process."
              centered
              className="mb-16"
            />
          </div>
          
          <div className="col-span-12">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {developerFeatures.map((feature, index) => (
                <FeatureCard
                  key={feature.title}
                  {...feature}
                  delay={index * 0.1}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Integration Features */}
      <section className="py-24">
        <div className="container-grid">
          <div className="col-span-12">
            <SectionHeader
              subtitle="Integrations"
              title="Connect Everything"
              description="Seamlessly integrate with your favorite tools and services to create a unified development ecosystem."
              centered
              className="mb-16"
            />
          </div>
          
          <div className="col-span-12">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {integrationFeatures.map((feature, index) => (
                <FeatureCard
                  key={feature.title}
                  {...feature}
                  delay={index * 0.1}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Technical Specs */}
      <section className="py-24 bg-muted/30">
        <div className="container-grid">
          <div className="col-span-12 lg:col-span-6">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-8"
            >
              <SectionHeader
                subtitle="Technical Specifications"
                title="Built on Modern Standards"
                description="Our platform is built using the latest technologies and follows industry best practices for performance, security, and scalability."
              />
              
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h4 className="font-semibold text-foreground">Frontend</h4>
                  <ul className="space-y-2">
                    {['React 18+', 'TypeScript', 'Vite', 'Tailwind CSS'].map((tech) => (
                      <li key={tech} className="flex items-center text-sm text-muted-foreground">
                        <Cpu className="h-3 w-3 mr-2 text-primary" />
                        {tech}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div className="space-y-4">
                  <h4 className="font-semibold text-foreground">Backend</h4>
                  <ul className="space-y-2">
                    {['Node.js', 'PostgreSQL', 'Redis', 'Docker'].map((tech) => (
                      <li key={tech} className="flex items-center text-sm text-muted-foreground">
                        <Database className="h-3 w-3 mr-2 text-primary" />
                        {tech}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </motion.div>
          </div>
          
          <div className="col-span-12 lg:col-span-6">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="grid grid-cols-2 gap-6"
            >
              {[
                { label: 'Uptime', value: '99.9%', icon: BarChart },
                { label: 'Global CDN', value: '150+', icon: Globe },
                { label: 'Load Time', value: '<100ms', icon: Zap },
                { label: 'Security', value: 'SOC 2', icon: Shield }
              ].map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.6, delay: 0.3 + index * 0.1 }}
                  className="glass p-6 rounded-2xl text-center space-y-2"
                >
                  <stat.icon className="h-8 w-8 text-primary mx-auto" />
                  <div className="text-2xl font-bold text-foreground">{stat.value}</div>
                  <div className="text-sm text-muted-foreground">{stat.label}</div>
                </motion.div>
              ))}
            </motion.div>
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
                  Ready to Experience These Features?
                </h2>
                <p className="text-xl text-white/80 max-w-2xl mx-auto">
                  Start building with our comprehensive feature set today. 
                  No credit card required.
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button variant="secondary" size="xl" asChild>
                  <Link to="/pricing">Get Started Free</Link>
                </Button>
                <Button variant="outline" size="xl" className="bg-white/10 border-white/20 text-white hover:bg-white/20" asChild>
                  <Link to="/showcase">View Examples</Link>
                </Button>
              </div>
            </motion.div>
          </div>
        </div>
      </section>
    </div>
  )
}