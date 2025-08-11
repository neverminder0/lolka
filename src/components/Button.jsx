import { motion } from 'framer-motion'
import { forwardRef } from 'react'

const buttonVariants = {
  primary: 'bg-primary-600 hover:bg-primary-700 text-white shadow-lg hover:shadow-xl',
  secondary: 'bg-secondary-400 hover:bg-secondary-500 text-white shadow-lg hover:shadow-xl',
  outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-600 hover:text-white',
  ghost: 'hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300',
  gradient: 'gradient-primary text-white shadow-glow',
}

const buttonSizes = {
  sm: 'px-4 py-2 text-sm',
  md: 'px-6 py-3 text-base',
  lg: 'px-8 py-4 text-lg',
  xl: 'px-10 py-5 text-xl',
}

const Button = forwardRef(({ 
  variant = 'primary', 
  size = 'md', 
  className = '', 
  children, 
  disabled = false,
  ...props 
}, ref) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-2xl transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-primary-500/50 disabled:opacity-50 disabled:cursor-not-allowed'
  
  const classes = `${baseClasses} ${buttonVariants[variant]} ${buttonSizes[size]} ${className}`

  return (
    <motion.button
      ref={ref}
      className={classes}
      disabled={disabled}
      whileHover={{ scale: disabled ? 1 : 1.02 }}
      whileTap={{ scale: disabled ? 1 : 0.98 }}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
      {...props}
    >
      {children}
    </motion.button>
  )
})

Button.displayName = 'Button'

export default Button

// Example usage:
// <Button variant="primary" size="lg">Get Started</Button>
// <Button variant="outline" size="md">Learn More</Button>
// <Button variant="gradient" size="xl">Try Now</Button>