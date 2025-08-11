import { motion } from 'framer-motion'

const badgeVariants = {
  primary: 'bg-primary-100 text-primary-800 dark:bg-primary-900/20 dark:text-primary-300',
  secondary: 'bg-secondary-100 text-secondary-800 dark:bg-secondary-900/20 dark:text-secondary-300',
  success: 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300',
  warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300',
  error: 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300',
  neutral: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300',
  gradient: 'gradient-primary text-white',
}

const badgeSizes = {
  sm: 'px-2 py-1 text-xs',
  md: 'px-3 py-1.5 text-sm',
  lg: 'px-4 py-2 text-base',
}

const Badge = ({ 
  variant = 'primary', 
  size = 'md', 
  className = '', 
  children,
  animated = true,
  ...props 
}) => {
  const baseClasses = 'inline-flex items-center font-medium rounded-full transition-all duration-200'
  const classes = `${baseClasses} ${badgeVariants[variant]} ${badgeSizes[size]} ${className}`

  if (animated) {
    return (
      <motion.span
        className={classes}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        transition={{ type: "spring", stiffness: 400, damping: 17 }}
        {...props}
      >
        {children}
      </motion.span>
    )
  }

  return (
    <span className={classes} {...props}>
      {children}
    </span>
  )
}

export default Badge

// Example usage:
// <Badge variant="primary" size="md">New</Badge>
// <Badge variant="gradient" size="lg">Pro</Badge>
// <Badge variant="success" size="sm">Active</Badge>