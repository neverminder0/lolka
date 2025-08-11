import { RouterProvider } from 'react-router-dom'
import { ThemeProvider } from './hooks/useTheme'
import { router } from './routes'

/**
 * Main App component with routing and theme providers
 */
function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="ui-theme">
      <RouterProvider router={router} />
    </ThemeProvider>
  )
}

export default App
