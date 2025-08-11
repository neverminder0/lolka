import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { 
  ArrowRight, 
  Play, 
  Star, 
  Zap, 
  Shield, 
  Palette, 
  Smartphone,
  Globe,
  Rocket
} from 'lucide-react'
import Button from '../components/Button'
import Badge from '../components/Badge'
import SectionHeader from '../components/SectionHeader'
import FeatureCard from '../components/FeatureCard'

const features = [
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Optimized performance with modern build tools and best practices for blazing fast load times.',
  },
  {
    icon: Shield,
    title: 'Secure & Reliable',
    description: 'Built with security in mind, following industry standards for data protection and reliability.',
  },
  {
    icon: Palette,
    title: 'Beautiful Design',
    description: 'Cutting-edge UI design with smooth animations and responsive layouts that look stunning.',
  },
  {
    icon: Smartphone,
    title: 'Mobile First',
    description: 'Fully responsive design that provides an excellent experience across all devices and screen sizes.',
  },
  {
    icon: Globe,
    title: 'Global Ready',
    description: 'Internationalization support with accessibility features and SEO optimization built-in.',
  },
  {
    icon: Rocket,
    title: 'Future Proof',
    description: 'Built with the latest technologies and patterns to ensure your project stays current.',
  },
]

const testimonials = [
  {
    name: 'Sarah Johnson',
    role: 'CEO, TechFlow',
    image: '/api/placeholder/64/64',
    content: 'This website template exceeded our expectations. The design is stunning and the performance is incredible.',
    rating: 5,
  },
  {
    name: 'Michael Chen',
    role: 'Design Director, CreativeStudio',
    image: '/api/placeholder/64/64',
    content: 'The attention to detail and smooth animations make this one of the best React templates I\'ve used.',
    rating: 5,
  },
  {
    name: 'Emily Rodriguez',
    role: 'Product Manager, InnovateApp',
    image: '/api/placeholder/64/64',
    content: 'Easy to customize and incredibly well-documented. Our team was able to launch quickly.',
    rating: 5,
  },
]

const stats = [
  { value: '10K+', label: 'Happy Customers' },
  { value: '99.9%', label: 'Uptime' },
  { value: '50ms', label: 'Response Time' },
  { value: '24/7', label: 'Support' },
]

const Home = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
        {/* Background Elements */}
        <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23e5e7eb" fill-opacity="0.1"%3E%3Ccircle cx="30" cy="30" r="1"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] dark:opacity-20"></div>
        
        <div className="container-custom section-padding relative">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Hero Content */}
            <motion.div
              className="text-center lg:text-left"
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            >
              <motion.div
                className="flex justify-center lg:justify-start mb-6"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <Badge variant="gradient" size="lg">
                  ✨ New Launch - React 18 Ready
                </Badge>
              </motion.div>

              <motion.h1
                className="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-bold text-gray-900 dark:text-white mb-6 leading-tight"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.3 }}
              >
                <span className="text-gradient">Cutting Edge</span>
                <br />
                Web Experience
              </motion.h1>

              <motion.p
                className="text-xl text-gray-600 dark:text-gray-400 mb-8 leading-relaxed max-w-2xl"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.4 }}
              >
                Build stunning, modern websites with our cutting-edge React template. 
                Features elegant animations, responsive design, and beautiful UI components.
              </motion.p>

              <motion.div
                className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.5 }}
              >
                <Button variant="gradient" size="xl" className="group">
                  Get Started Free
                  <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                </Button>
                <Button variant="outline" size="xl" className="group">
                  <Play className="w-5 h-5 mr-2" />
                  Watch Demo
                </Button>
              </motion.div>

              {/* Stats */}
              <motion.div
                className="grid grid-cols-2 sm:grid-cols-4 gap-6 mt-12 pt-12 border-t border-gray-200 dark:border-gray-700"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.6 }}
              >
                {stats.map((stat, index) => (
                  <div key={stat.label} className="text-center lg:text-left">
                    <div className="text-2xl sm:text-3xl font-bold text-gradient mb-1">
                      {stat.value}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      {stat.label}
                    </div>
                  </div>
                ))}
              </motion.div>
            </motion.div>

            {/* Hero Visual */}
            <motion.div
              className="relative"
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              <motion.div
                className="relative z-10 p-8 glass-effect rounded-2xl shadow-glow"
                whileHover={{ y: -10 }}
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
              >
                <div className="aspect-square bg-gradient-to-br from-primary-400 via-secondary-400 to-primary-600 rounded-2xl p-12 flex items-center justify-center">
                  <motion.div
                    className="text-white text-center"
                    animate={{ 
                      rotate: [0, 5, -5, 0],
                      scale: [1, 1.05, 1] 
                    }}
                    transition={{ 
                      duration: 4, 
                      repeat: Infinity,
                      ease: "easeInOut" 
                    }}
                  >
                    <Zap className="w-24 h-24 mx-auto mb-4" />
                    <div className="text-2xl font-bold">React 18</div>
                    <div className="text-lg opacity-90">Powered</div>
                  </motion.div>
                </div>
              </motion.div>

              {/* Floating Elements */}
              <motion.div
                className="absolute -top-4 -right-4 w-24 h-24 bg-secondary-400 rounded-full opacity-20 blur-xl"
                animate={{ 
                  scale: [1, 1.2, 1],
                  opacity: [0.2, 0.3, 0.2] 
                }}
                transition={{ 
                  duration: 3, 
                  repeat: Infinity,
                  ease: "easeInOut" 
                }}
              />
              <motion.div
                className="absolute -bottom-6 -left-6 w-32 h-32 bg-primary-500 rounded-full opacity-10 blur-2xl"
                animate={{ 
                  scale: [1, 1.3, 1],
                  opacity: [0.1, 0.2, 0.1] 
                }}
                transition={{ 
                  duration: 4, 
                  repeat: Infinity,
                  ease: "easeInOut",
                  delay: 1 
                }}
              />
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="section-padding bg-white dark:bg-gray-900">
        <div className="container-custom">
          <SectionHeader
            badge="Features"
            title="Everything you need to succeed"
            description="Our comprehensive suite of features is designed to help you build amazing web experiences with ease and efficiency."
            className="mb-16"
          />

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
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

      {/* Testimonials Section */}
      <section className="section-padding bg-gray-50 dark:bg-gray-800">
        <div className="container-custom">
          <SectionHeader
            title="What our customers say"
            description="Don't just take our word for it. Here's what real customers have to say about their experience."
            className="mb-16"
          />

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={testimonial.name}
                className="p-8 glass-effect rounded-2xl"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                <div className="flex items-center gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>
                
                <p className="text-gray-600 dark:text-gray-400 mb-6 leading-relaxed">
                  "{testimonial.content}"
                </p>
                
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-r from-primary-400 to-secondary-400 flex items-center justify-center text-white font-semibold">
                    {testimonial.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900 dark:text-white">
                      {testimonial.name}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      {testimonial.role}
                    </div>
                  </div>
                </div>
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
              Join thousands of developers who are already building amazing experiences with our platform.
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

export default Home