import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Calendar, Clock, ArrowLeft, User, Share2 } from 'lucide-react'
import Badge from '../components/Badge'
import Button from '../components/Button'

// This would normally come from an API or CMS
const getBlogPost = (slug) => {
  const posts = {
    'building-modern-react-apps': {
      title: 'Building Modern React Applications with Best Practices',
      content: `
        <h2>Introduction</h2>
        <p>React has evolved significantly over the years, and with it, the best practices for building modern applications. In this comprehensive guide, we'll explore the latest patterns, hooks, and optimization techniques that will help you build scalable React applications.</p>
        
        <h2>Key Concepts</h2>
        <p>Modern React development focuses on several key areas:</p>
        <ul>
          <li>Functional components and hooks</li>
          <li>State management with Context API and reducers</li>
          <li>Performance optimization techniques</li>
          <li>Testing strategies</li>
          <li>Code organization and architecture</li>
        </ul>
        
        <h2>Performance Optimization</h2>
        <p>Performance is crucial for user experience. Here are some essential techniques:</p>
        <p>React.memo() helps prevent unnecessary re-renders by memoizing component output. Use it when your component renders the same result given the same props.</p>
        
        <h2>Conclusion</h2>
        <p>Building modern React applications requires understanding these core concepts and best practices. By following these guidelines, you'll create more maintainable, performant, and scalable applications.</p>
      `,
      author: 'Sarah Johnson',
      category: 'Development',
      readTime: '8 min read',
      publishDate: '2024-01-15',
      image: 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&h=400&fit=crop'
    }
  }
  
  return posts[slug] || {
    title: 'Post Not Found',
    content: '<p>The blog post you are looking for does not exist.</p>',
    author: 'Unknown',
    category: 'General',
    readTime: '1 min read',
    publishDate: '2024-01-01',
    image: 'https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=800&h=400&fit=crop'
  }
}

const BlogPost = () => {
  const { slug } = useParams()
  const post = getBlogPost(slug)

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
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-4xl mx-auto"
          >
            {/* Back Button */}
            <Link
              to="/blog"
              className="inline-flex items-center gap-2 text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors duration-200 mb-8"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Blog
            </Link>

            {/* Article Header */}
            <article className="glass-effect rounded-2xl overflow-hidden">
              <div className="relative">
                <img
                  src={post.image}
                  alt={post.title}
                  className="w-full h-64 sm:h-80 object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
                
                <div className="absolute bottom-6 left-6 right-6">
                  <Badge variant="gradient" size="md" className="mb-4">
                    {post.category}
                  </Badge>
                  <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-4 leading-tight">
                    {post.title}
                  </h1>
                  
                  <div className="flex flex-wrap items-center gap-6 text-white/90">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-r from-primary-400 to-secondary-400 flex items-center justify-center text-white font-semibold">
                        {post.author.split(' ').map(n => n[0]).join('')}
                      </div>
                      <span className="font-medium">{post.author}</span>
                    </div>
                    
                    <div className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      {new Date(post.publishDate).toLocaleDateString()}
                    </div>
                    
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {post.readTime}
                    </div>
                  </div>
                </div>
              </div>

              {/* Article Content */}
              <div className="p-8 sm:p-12">
                <div className="flex justify-between items-center mb-8">
                  <div className="flex items-center gap-4">
                    <Button variant="outline" size="sm">
                      <Share2 className="w-4 h-4 mr-2" />
                      Share
                    </Button>
                  </div>
                </div>

                <motion.div
                  className="prose prose-lg max-w-none dark:prose-invert prose-headings:text-gray-900 dark:prose-headings:text-white prose-p:text-gray-600 dark:prose-p:text-gray-400 prose-a:text-primary-600 dark:prose-a:text-primary-400 prose-strong:text-gray-900 dark:prose-strong:text-white"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                  dangerouslySetInnerHTML={{ __html: post.content }}
                />
              </div>
            </article>

            {/* Related Posts */}
            <motion.div
              className="mt-16"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-8">
                Related Posts
              </h2>
              
              <div className="grid md:grid-cols-2 gap-8">
                {/* Mock related posts */}
                {[
                  {
                    title: 'Advanced Tailwind CSS Tips and Tricks',
                    slug: 'tailwind-css-tips',
                    category: 'Design',
                    readTime: '5 min read',
                    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=250&fit=crop'
                  },
                  {
                    title: 'Creating Beautiful Animations with Framer Motion',
                    slug: 'framer-motion-animations',
                    category: 'Animation',
                    readTime: '10 min read',
                    image: 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=250&fit=crop'
                  }
                ].map((relatedPost, index) => (
                  <motion.div
                    key={relatedPost.slug}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.5 + index * 0.1 }}
                    whileHover={{ y: -5 }}
                  >
                    <Link to={`/blog/${relatedPost.slug}`} className="block group">
                      <div className="glass-effect rounded-2xl overflow-hidden hover:shadow-glow transition-all duration-300">
                        <img
                          src={relatedPost.image}
                          alt={relatedPost.title}
                          className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                        
                        <div className="p-6">
                          <Badge variant="neutral" size="sm" className="mb-3">
                            {relatedPost.category}
                          </Badge>
                          
                          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-200">
                            {relatedPost.title}
                          </h3>
                          
                          <div className="flex items-center gap-1 text-sm text-gray-600 dark:text-gray-400">
                            <Clock className="w-4 h-4" />
                            {relatedPost.readTime}
                          </div>
                        </div>
                      </div>
                    </Link>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>
    </motion.div>
  )
}

export default BlogPost