import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Calendar, Clock, ArrowRight, User } from 'lucide-react'
import SectionHeader from '../components/SectionHeader'
import Badge from '../components/Badge'

const blogPosts = [
  {
    id: 1,
    slug: 'building-modern-react-apps',
    title: 'Building Modern React Applications with Best Practices',
    excerpt: 'Learn how to build scalable React applications using the latest patterns, hooks, and performance optimization techniques.',
    content: 'Full article content here...',
    author: 'Sarah Johnson',
    category: 'Development',
    readTime: '8 min read',
    publishDate: '2024-01-15',
    image: 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=600&h=400&fit=crop',
    featured: true
  },
  {
    id: 2,
    slug: 'tailwind-css-tips',
    title: 'Advanced Tailwind CSS Tips and Tricks',
    excerpt: 'Discover advanced Tailwind CSS techniques to create beautiful, responsive designs with minimal custom CSS.',
    content: 'Full article content here...',
    author: 'Michael Chen',
    category: 'Design',
    readTime: '5 min read',
    publishDate: '2024-01-12',
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
    featured: false
  },
  {
    id: 3,
    slug: 'framer-motion-animations',
    title: 'Creating Beautiful Animations with Framer Motion',
    excerpt: 'Master the art of web animations using Framer Motion to create engaging user experiences.',
    content: 'Full article content here...',
    author: 'Emily Rodriguez',
    category: 'Animation',
    readTime: '10 min read',
    publishDate: '2024-01-10',
    image: 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&h=400&fit=crop',
    featured: true
  },
  {
    id: 4,
    slug: 'web-performance-optimization',
    title: 'Web Performance Optimization in 2024',
    excerpt: 'Essential techniques for optimizing web performance, including Core Web Vitals and modern loading strategies.',
    content: 'Full article content here...',
    author: 'David Kim',
    category: 'Performance',
    readTime: '12 min read',
    publishDate: '2024-01-08',
    image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=400&fit=crop',
    featured: false
  },
  {
    id: 5,
    slug: 'dark-mode-implementation',
    title: 'Implementing Dark Mode in React Applications',
    excerpt: 'A complete guide to implementing dark mode with system preference detection and smooth transitions.',
    content: 'Full article content here...',
    author: 'Lisa Zhang',
    category: 'Development',
    readTime: '7 min read',
    publishDate: '2024-01-05',
    image: 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=600&h=400&fit=crop',
    featured: false
  },
  {
    id: 6,
    slug: 'responsive-design-principles',
    title: 'Modern Responsive Design Principles',
    excerpt: 'Learn the fundamental principles of responsive design and how to create layouts that work on any device.',
    content: 'Full article content here...',
    author: 'Alex Thompson',
    category: 'Design',
    readTime: '9 min read',
    publishDate: '2024-01-03',
    image: 'https://images.unsplash.com/photo-1494232410401-ad00d5433cfa?w=600&h=400&fit=crop',
    featured: false
  }
]

const categories = ['All', 'Development', 'Design', 'Animation', 'Performance']

const Blog = () => {
  const featuredPosts = blogPosts.filter(post => post.featured)
  const regularPosts = blogPosts.filter(post => !post.featured)

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
            badge="Blog"
            title="Latest insights and tutorials"
            description="Stay up to date with the latest trends, best practices, and tutorials in web development and design."
            className="mb-16"
          />

          {/* Featured Posts */}
          <div className="mb-16">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-8">Featured Posts</h2>
            <div className="grid lg:grid-cols-2 gap-8">
              {featuredPosts.map((post, index) => (
                <motion.article
                  key={post.id}
                  className="group cursor-pointer"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  whileHover={{ y: -5 }}
                >
                  <Link to={`/blog/${post.slug}`} className="block">
                    <div className="glass-effect rounded-2xl overflow-hidden hover:shadow-glow transition-all duration-300">
                      <div className="relative">
                        <img
                          src={post.image}
                          alt={post.title}
                          className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                        <div className="absolute top-4 left-4">
                          <Badge variant="gradient" size="md">
                            Featured
                          </Badge>
                        </div>
                      </div>
                      
                      <div className="p-8">
                        <div className="flex items-center gap-4 mb-4 text-sm text-gray-600 dark:text-gray-400">
                          <Badge variant="secondary" size="sm">
                            {post.category}
                          </Badge>
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            {new Date(post.publishDate).toLocaleDateString()}
                          </div>
                          <div className="flex items-center gap-1">
                            <Clock className="w-4 h-4" />
                            {post.readTime}
                          </div>
                        </div>
                        
                        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-200">
                          {post.title}
                        </h3>
                        
                        <p className="text-gray-600 dark:text-gray-400 leading-relaxed mb-6">
                          {post.excerpt}
                        </p>
                        
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-primary-400 to-secondary-400 flex items-center justify-center text-white text-sm font-semibold">
                              {post.author.split(' ').map(n => n[0]).join('')}
                            </div>
                            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                              {post.author}
                            </span>
                          </div>
                          
                          <div className="flex items-center gap-2 text-primary-600 dark:text-primary-400 font-medium group-hover:gap-3 transition-all duration-200">
                            <span>Read more</span>
                            <ArrowRight className="w-4 h-4" />
                          </div>
                        </div>
                      </div>
                    </div>
                  </Link>
                </motion.article>
              ))}
            </div>
          </div>

          {/* Regular Posts */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-8">All Posts</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {regularPosts.map((post, index) => (
                <motion.article
                  key={post.id}
                  className="group cursor-pointer"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.3 + index * 0.1 }}
                  whileHover={{ y: -5 }}
                >
                  <Link to={`/blog/${post.slug}`} className="block">
                    <div className="glass-effect rounded-2xl overflow-hidden hover:shadow-glow transition-all duration-300 h-full">
                      <div className="relative">
                        <img
                          src={post.image}
                          alt={post.title}
                          className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                      </div>
                      
                      <div className="p-6">
                        <div className="flex items-center gap-4 mb-3 text-sm text-gray-600 dark:text-gray-400">
                          <Badge variant="neutral" size="sm">
                            {post.category}
                          </Badge>
                          <div className="flex items-center gap-1">
                            <Clock className="w-4 h-4" />
                            {post.readTime}
                          </div>
                        </div>
                        
                        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-3 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-200 line-clamp-2">
                          {post.title}
                        </h3>
                        
                        <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed mb-4 line-clamp-3">
                          {post.excerpt}
                        </p>
                        
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <div className="w-6 h-6 rounded-full bg-gradient-to-r from-primary-400 to-secondary-400 flex items-center justify-center text-white text-xs font-semibold">
                              {post.author.split(' ').map(n => n[0]).join('')}
                            </div>
                            <span className="text-xs text-gray-600 dark:text-gray-400">
                              {post.author}
                            </span>
                          </div>
                          
                          <div className="text-xs text-gray-500 dark:text-gray-500">
                            {new Date(post.publishDate).toLocaleDateString()}
                          </div>
                        </div>
                      </div>
                    </div>
                  </Link>
                </motion.article>
              ))}
            </div>
          </div>
        </div>
      </section>
    </motion.div>
  )
}

export default Blog