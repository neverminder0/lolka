import { motion } from 'framer-motion'
import { ArrowRight, Star, Users, Zap, Shield, Rocket, Award } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { Link } from 'react-router-dom'

const features = [
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Built for speed with modern optimization techniques'
  },
  {
    icon: Shield,
    title: 'Secure by Default',
    description: 'Enterprise-grade security built into every component'
  },
  {
    icon: Users,
    title: 'Team Collaboration',
    description: 'Work together seamlessly with real-time updates'
  },
  {
    icon: Rocket,
    title: 'Easy Deployment',
    description: 'Deploy anywhere with our simple one-click solutions'
  }
]

const companies = [
  'TechCorp', 'DataFlow', 'CloudBase', 'InnovateLab', 'FutureStack', 'DevHub', 'CodeCraft', 'WebFlow'
]

const testimonials = [
  { text: "This platform revolutionized our workflow", author: "Sarah Chen", company: "TechCorp" },
  { text: "Incredible performance and reliability", author: "Mike Johnson", company: "DataFlow" },
  { text: "Best investment we've made this year", author: "Emily Davis", company: "CloudBase" },
  { text: "Game-changing technology", author: "Alex Rodriguez", company: "InnovateLab" }
]

/**
 * Home page with multiple hero sections, features, and dynamic content
 */
export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Main Hero Section */}
      <section className="relative overflow-hidden bg-gradient-mesh pt-24 pb-16">
        <div className="absolute inset-0 bg-grid-white/[0.02] bg-[size:60px_60px]" />
        <div className="container-grid relative z-10">
          <div className="col-span-12 lg:col-span-8 lg:col-start-3 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-8"
            >
              <Badge variant="gradient" className="mb-4">
                🚀 New Release v2.0
              </Badge>
              
              <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight">
                Build Amazing{' '}
                <span className="text-gradient">Digital Experiences</span>
              </h1>
              
              <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                Create stunning websites and applications with our modern toolkit. 
                Fast, secure, and beautifully designed.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button variant="gradient" size="xl" asChild>
                  <Link to="/pricing">
                    Get Started Free
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                </Button>
                <Button variant="outline" size="xl" asChild>
                  <Link to="/showcase">View Examples</Link>
                </Button>
              </div>
              
              <div className="flex items-center justify-center space-x-2 text-sm text-muted-foreground">
                <div className="flex">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>
                <span>5.0 rating from 1000+ customers</span>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Company Marquee */}
      <section className="py-12 bg-muted/30">
        <div className="container-grid">
          <div className="col-span-12 text-center mb-8">
            <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
              Trusted by innovative companies
            </p>
          </div>
        </div>
        <div className="marquee">
          <div className="marquee-content">
            {companies.map((company, index) => (
              <div key={index} className="flex-shrink-0 mx-8">
                <span className="text-2xl font-bold text-muted-foreground/60 hover:text-foreground transition-colors">
                  {company}
                </span>
              </div>
            ))}
          </div>
          <div className="marquee-content2">
            {companies.map((company, index) => (
              <div key={index} className="flex-shrink-0 mx-8">
                <span className="text-2xl font-bold text-muted-foreground/60 hover:text-foreground transition-colors">
                  {company}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24">
        <div className="container-grid">
          <div className="col-span-12">
            <SectionHeader
              subtitle="Why Choose Us"
              title="Powerful Features for Modern Development"
              description="Everything you need to build exceptional digital experiences, from concept to deployment."
              centered
              className="mb-16"
            />
          </div>
          
          <div className="col-span-12">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="group p-6 rounded-2xl glass hover:glass-strong transition-all duration-300 hover:scale-105"
                >
                  <div className="space-y-4">
                    <div className="p-3 rounded-xl bg-primary/10 w-fit group-hover:bg-primary/20 transition-colors">
                      <feature.icon className="h-6 w-6 text-primary" />
                    </div>
                    <h3 className="text-xl font-semibold">{feature.title}</h3>
                    <p className="text-muted-foreground">{feature.description}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Second Hero Section */}
      <section className="py-24 bg-muted/30">
        <div className="container-grid">
          <div className="col-span-12 lg:col-span-6">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-8"
            >
              <Badge variant="outline">
                <Award className="h-3 w-3 mr-2" />
                Award Winning Design
              </Badge>
              
              <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
                Designed for{' '}
                <span className="text-gradient">Developers</span>
              </h2>
              
              <p className="text-lg text-muted-foreground">
                Built with modern technologies and best practices. Our platform provides 
                everything you need to create, deploy, and scale your applications with confidence.
              </p>
              
              <ul className="space-y-3">
                {['TypeScript & React', 'Modern CSS & Animations', 'Performance Optimized', 'Accessibility First'].map((item) => (
                  <li key={item} className="flex items-center">
                    <div className="h-2 w-2 rounded-full bg-primary mr-3" />
                    <span className="text-muted-foreground">{item}</span>
                  </li>
                ))}
              </ul>
              
              <div className="flex gap-4">
                <Button variant="default" size="lg" asChild>
                  <Link to="/features">Learn More</Link>
                </Button>
                <Button variant="ghost" size="lg" asChild>
                  <Link to="/showcase">See Examples</Link>
                </Button>
              </div>
            </motion.div>
          </div>
          
          <div className="col-span-12 lg:col-span-6">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="relative"
            >
              <div className="aspect-square rounded-3xl glass overflow-hidden">
                <div className="absolute inset-4 rounded-2xl bg-gradient-primary opacity-20" />
                <div className="absolute inset-8 rounded-xl bg-gradient-secondary opacity-30" />
                <div className="absolute inset-12 rounded-lg glass-strong flex items-center justify-center">
                  <div className="text-center space-y-4">
                    <div className="text-4xl font-bold text-gradient">2M+</div>
                    <div className="text-sm text-muted-foreground">Active Users</div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-24">
        <div className="container-grid">
          <div className="col-span-12">
            <SectionHeader
              subtitle="Testimonials"
              title="What Our Customers Say"
              centered
              className="mb-16"
            />
          </div>
          
          <div className="col-span-12">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {testimonials.map((testimonial, index) => (
                <motion.blockquote
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="p-6 rounded-2xl glass space-y-4"
                >
                  <div className="flex">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    ))}
                  </div>
                  <p className="text-foreground">&ldquo;{testimonial.text}&rdquo;</p>
                  <footer className="text-sm text-muted-foreground">
                    <cite className="font-medium">{testimonial.author}</cite>
                    <br />
                    {testimonial.company}
                  </footer>
                </motion.blockquote>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-mesh">
        <div className="container-grid">
          <div className="col-span-12 lg:col-span-8 lg:col-start-3 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-8"
            >
              <h2 className="text-3xl md:text-5xl font-bold tracking-tight text-white">
                Ready to Get Started?
              </h2>
              <p className="text-xl text-white/80">
                Join thousands of developers building amazing experiences.
              </p>
              <Button variant="secondary" size="xl" asChild>
                <Link to="/pricing">
                  Start Building Today
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
            </motion.div>
          </div>
        </div>
      </section>
    </div>
  )
}