import { motion } from 'framer-motion'

const LoadingSpinner = ({ size = 'lg', className = '' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16',
  }

  return (
    <div className={`flex items-center justify-center min-h-screen ${className}`}>
      <motion.div
        className={`${sizeClasses[size]} rounded-full border-4 border-gray-200 dark:border-gray-700`}
        style={{
          borderTopColor: 'transparent',
          background: 'conic-gradient(from 0deg, #7C3AED, #22D3EE, #7C3AED)',
        }}
        animate={{ rotate: 360 }}
        transition={{
          duration: 1,
          repeat: Infinity,
          ease: "linear"
        }}
      />
    </div>
  )
}

export default LoadingSpinner