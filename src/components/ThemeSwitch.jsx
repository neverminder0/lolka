import { motion } from 'framer-motion'
import { Sun, Moon } from 'lucide-react'
import { useTheme } from '../hooks/useTheme'

const ThemeSwitch = ({ className = '' }) => {
  const { theme, toggleTheme } = useTheme()
  const isDark = theme === 'dark'

  return (
    <motion.button
      onClick={toggleTheme}
      className={`relative inline-flex items-center justify-center w-14 h-8 rounded-full p-1 transition-colors duration-300 focus:outline-none focus:ring-4 focus:ring-primary-500/50 ${
        isDark 
          ? 'bg-gray-700 hover:bg-gray-600' 
          : 'bg-gray-200 hover:bg-gray-300'
      } ${className}`}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
      role="switch"
      aria-checked={isDark}
    >
      {/* Background track */}
      <motion.div
        className={`absolute inset-1 rounded-full transition-colors duration-300 ${
          isDark ? 'bg-primary-600' : 'bg-yellow-400'
        }`}
        initial={false}
        animate={{
          opacity: isDark ? 1 : 1,
        }}
        transition={{ duration: 0.3 }}
      />
      
      {/* Switch thumb */}
      <motion.div
        className="relative z-10 flex items-center justify-center w-6 h-6 bg-white rounded-full shadow-lg"
        initial={false}
        animate={{
          x: isDark ? 20 : 0,
        }}
        transition={{
          type: "spring",
          stiffness: 500,
          damping: 30
        }}
      >
        {/* Icon container */}
        <motion.div
          initial={false}
          animate={{
            scale: isDark ? 0 : 1,
            rotate: isDark ? 180 : 0,
          }}
          transition={{ duration: 0.2 }}
          className="absolute"
        >
          <Sun size={14} className="text-yellow-600" />
        </motion.div>
        
        <motion.div
          initial={false}
          animate={{
            scale: isDark ? 1 : 0,
            rotate: isDark ? 0 : -180,
          }}
          transition={{ duration: 0.2 }}
          className="absolute"
        >
          <Moon size={14} className="text-primary-600" />
        </motion.div>
      </motion.div>
    </motion.button>
  )
}

export default ThemeSwitch

// Example usage:
// <ThemeSwitch />
// <ThemeSwitch className="ml-4" />