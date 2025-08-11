import { Outlet } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import Navbar from './Navbar'
import Footer from './Footer'
import { ThemeProvider } from '../hooks/useTheme'

const RootLayout = () => {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-300">
        <Navbar />
        
        <main className="flex-1">
          <AnimatePresence mode="wait">
            <Outlet />
          </AnimatePresence>
        </main>
        
        <Footer />
      </div>
    </ThemeProvider>
  )
}

export default RootLayout