import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, ExternalLink, Github, Eye } from 'lucide-react'
import SectionHeader from '../components/SectionHeader'
import Badge from '../components/Badge'

const projects = [
  {
    id: 1,
    title: 'E-commerce Platform',
    category: 'Web App',
    image: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=300&fit=crop',
    description: 'Modern e-commerce platform built with React and Node.js featuring real-time inventory management.',
    tags: ['React', 'Node.js', 'MongoDB', 'Stripe'],
    liveUrl: '#',
    githubUrl: '#'
  },
  {
    id: 2,
    title: 'Dashboard Analytics',
    category: 'Dashboard',
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=500&fit=crop',
    description: 'Comprehensive analytics dashboard with real-time data visualization and interactive charts.',
    tags: ['React', 'D3.js', 'TypeScript', 'Firebase'],
    liveUrl: '#',
    githubUrl: '#'
  },
  {
    id: 3,
    title: 'Social Media App',
    category: 'Mobile App',
    image: 'https://images.unsplash.com/photo-1611262588024-d12430b98920?w=400&h=400&fit=crop',
    description: 'Social media application with real-time messaging, post sharing, and user engagement features.',
    tags: ['React Native', 'Socket.io', 'PostgreSQL'],
    liveUrl: '#',
    githubUrl: '#'
  },
  {
    id: 4,
    title: 'Portfolio Website',
    category: 'Website',
    image: 'https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=400&h=350&fit=crop',
    description: 'Elegant portfolio website showcasing creative work with smooth animations and modern design.',
    tags: ['Next.js', 'Framer Motion', 'Tailwind CSS'],
    liveUrl: '#',
    githubUrl: '#'
  },
  {
    id: 5,
    title: 'Learning Platform',
    category: 'Web App',
    image: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=400&h=450&fit=crop',
    description: 'Online learning platform with video courses, quizzes, and progress tracking.',
    tags: ['React', 'Video.js', 'Express', 'MySQL'],
    liveUrl: '#',
    githubUrl: '#'
  },
  {
    id: 6,
    title: 'Weather App',
    category: 'Mobile App',
    image: 'https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=400&h=300&fit=crop',
    description: 'Beautiful weather application with location-based forecasts and interactive maps.',
    tags: ['React Native', 'OpenWeather API', 'MapBox'],
    liveUrl: '#',
    githubUrl: '#'
  }
]

const categories = ['All', 'Web App', 'Mobile App', 'Dashboard', 'Website']

const Showcase = () => {
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [selectedProject, setSelectedProject] = useState(null)

  const filteredProjects = selectedCategory === 'All' 
    ? projects 
    : projects.filter(project => project.category === selectedCategory)

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
            badge="Showcase"
            title="Our latest work"
            description="Explore our portfolio of beautiful, functional websites and applications built with cutting-edge technology."
            className="mb-12"
          />

          {/* Category Filter */}
          <motion.div
            className="flex flex-wrap justify-center gap-4 mb-16"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            {categories.map((category) => (
              <motion.button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-6 py-3 rounded-2xl font-medium transition-all duration-200 ${
                  selectedCategory === category
                    ? 'bg-primary-600 text-white shadow-lg'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {category}
              </motion.button>
            ))}
          </motion.div>

          {/* Projects Grid */}
          <motion.div 
            className="columns-1 md:columns-2 lg:columns-3 gap-8 space-y-8"
            layout
          >
            <AnimatePresence>
              {filteredProjects.map((project, index) => (
                <motion.div
                  key={project.id}
                  className="break-inside-avoid group cursor-pointer"
                  layout
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  onClick={() => setSelectedProject(project)}
                >
                  <div className="relative overflow-hidden rounded-2xl glass-effect hover:shadow-glow transition-all duration-300">
                    <div className="relative">
                      <img
                        src={project.image}
                        alt={project.title}
                        className="w-full h-auto object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                      
                      {/* Hover Overlay */}
                      <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                        <div className="flex gap-3">
                          <motion.button
                            className="p-3 bg-white/20 backdrop-blur-sm rounded-full text-white hover:bg-white/30 transition-colors duration-200"
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                          >
                            <Eye className="w-5 h-5" />
                          </motion.button>
                          <motion.a
                            href={project.liveUrl}
                            className="p-3 bg-white/20 backdrop-blur-sm rounded-full text-white hover:bg-white/30 transition-colors duration-200"
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                          >
                            <ExternalLink className="w-5 h-5" />
                          </motion.a>
                          <motion.a
                            href={project.githubUrl}
                            className="p-3 bg-white/20 backdrop-blur-sm rounded-full text-white hover:bg-white/30 transition-colors duration-200"
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                          >
                            <Github className="w-5 h-5" />
                          </motion.a>
                        </div>
                      </div>
                    </div>

                    <div className="p-6">
                      <div className="flex items-center justify-between mb-3">
                        <Badge variant="secondary" size="sm">
                          {project.category}
                        </Badge>
                      </div>
                      
                      <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-200">
                        {project.title}
                      </h3>
                      
                      <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed mb-4">
                        {project.description}
                      </p>

                      <div className="flex flex-wrap gap-2">
                        {project.tags.map((tag) => (
                          <span
                            key={tag}
                            className="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </motion.div>
        </div>
      </section>

      {/* Project Modal */}
      <AnimatePresence>
        {selectedProject && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelectedProject(null)}
          >
            <motion.div
              className="relative w-full max-w-4xl glass-effect rounded-2xl overflow-hidden"
              initial={{ opacity: 0, scale: 0.8, y: 50 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.8, y: 50 }}
              transition={{ type: "spring", damping: 30, stiffness: 400 }}
              onClick={(e) => e.stopPropagation()}
            >
              <button
                onClick={() => setSelectedProject(null)}
                className="absolute top-4 right-4 z-10 p-2 bg-black/20 backdrop-blur-sm rounded-full text-white hover:bg-black/40 transition-colors duration-200"
              >
                <X className="w-6 h-6" />
              </button>

              <div className="grid md:grid-cols-2">
                <div className="relative">
                  <img
                    src={selectedProject.image}
                    alt={selectedProject.title}
                    className="w-full h-64 md:h-full object-cover"
                  />
                </div>
                
                <div className="p-8">
                  <Badge variant="secondary" size="md" className="mb-4">
                    {selectedProject.category}
                  </Badge>
                  
                  <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                    {selectedProject.title}
                  </h2>
                  
                  <p className="text-gray-600 dark:text-gray-400 leading-relaxed mb-6">
                    {selectedProject.description}
                  </p>

                  <div className="flex flex-wrap gap-2 mb-8">
                    {selectedProject.tags.map((tag) => (
                      <Badge key={tag} variant="neutral" size="sm">
                        {tag}
                      </Badge>
                    ))}
                  </div>

                  <div className="flex gap-4">
                    <motion.a
                      href={selectedProject.liveUrl}
                      className="flex items-center gap-2 px-6 py-3 bg-primary-600 text-white rounded-xl hover:bg-primary-700 transition-colors duration-200"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <ExternalLink className="w-5 h-5" />
                      View Live
                    </motion.a>
                    <motion.a
                      href={selectedProject.githubUrl}
                      className="flex items-center gap-2 px-6 py-3 border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <Github className="w-5 h-5" />
                      GitHub
                    </motion.a>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

export default Showcase