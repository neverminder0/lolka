import { motion } from 'framer-motion'

const FeatureCard = ({ 
  icon: Icon, 
  title, 
  description, 
  className = '',
  delay = 0,
  ...props 
}) => {
  return (
    <motion.div
      className={`p-8 rounded-2xl glass-effect hover:shadow-glow transition-all duration-300 group ${className}`}
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.6, delay, ease: "easeOut" }}
      whileHover={{ y: -5 }}
      {...props}
    >
      <motion.div
        className="flex items-center justify-center w-16 h-16 mb-6 rounded-2xl bg-gradient-to-r from-primary-600 to-secondary-400 group-hover:scale-110 transition-transform duration-300"
        whileHover={{ rotate: 5 }}
        transition={{ type: "spring", stiffness: 400, damping: 17 }}
      >
        {Icon && <Icon className="w-8 h-8 text-white" />}
      </motion.div>

      <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-300">
        {title}
      </h3>

      <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
        {description}
      </p>
    </motion.div>
  )
}

export default FeatureCard

// Example usage:
// import { Zap } from 'lucide-react'
// <FeatureCard 
//   icon={Zap}
//   title="Lightning Fast"
//   description="Experience blazing fast performance with our optimized codebase and modern architecture."
//   delay={0.1}
// />