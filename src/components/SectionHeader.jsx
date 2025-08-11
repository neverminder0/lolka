import { motion } from 'framer-motion'
import Badge from './Badge'

const SectionHeader = ({ 
  badge,
  title, 
  subtitle, 
  description,
  centered = true,
  className = '',
  ...props 
}) => {
  const containerClasses = `${centered ? 'text-center' : 'text-left'} ${className}`

  return (
    <motion.div
      className={containerClasses}
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      {...props}
    >
      {badge && (
        <motion.div
          className={`mb-4 ${centered ? 'flex justify-center' : 'flex'}`}
          initial={{ opacity: 0, scale: 0.8 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <Badge variant="gradient" size="md">
            {badge}
          </Badge>
        </motion.div>
      )}

      {subtitle && (
        <motion.p
          className="text-sm font-semibold text-primary-600 dark:text-primary-400 mb-2 tracking-wider uppercase"
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          {subtitle}
        </motion.p>
      )}

      <motion.h2
        className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 dark:text-white mb-6"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6, delay: 0.3 }}
      >
        <span className="text-gradient">{title}</span>
      </motion.h2>

      {description && (
        <motion.p
          className="text-lg text-gray-600 dark:text-gray-400 max-w-3xl mx-auto leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          {description}
        </motion.p>
      )}
    </motion.div>
  )
}

export default SectionHeader

// Example usage:
// <SectionHeader 
//   badge="New Feature"
//   subtitle="Introducing"
//   title="Revolutionary Design"
//   description="Experience the future of web design with our cutting-edge features and beautiful interface."
// />