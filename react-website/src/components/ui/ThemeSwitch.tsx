import { Button } from './Button'
import { useTheme } from '@/hooks/useTheme'
import { Sun, Moon, Monitor } from 'lucide-react'

/**
 * Theme switch component with cycling through light, dark, and system themes
 * Includes accessible icons and labels for each theme state
 */
export function ThemeSwitch() {
  const { theme, setTheme } = useTheme()

  const handleThemeChange = () => {
    if (theme === 'light') {
      setTheme('dark')
    } else if (theme === 'dark') {
      setTheme('system')
    } else {
      setTheme('light')
    }
  }

  const getIcon = () => {
    switch (theme) {
      case 'light':
        return <Sun className="h-4 w-4" />
      case 'dark':
        return <Moon className="h-4 w-4" />
      case 'system':
        return <Monitor className="h-4 w-4" />
      default:
        return <Sun className="h-4 w-4" />
    }
  }

  const getLabel = () => {
    switch (theme) {
      case 'light':
        return 'Switch to dark theme'
      case 'dark':
        return 'Switch to system theme'
      case 'system':
        return 'Switch to light theme'
      default:
        return 'Toggle theme'
    }
  }

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={handleThemeChange}
      aria-label={getLabel()}
      className="relative overflow-hidden"
    >
      <div className="transition-transform duration-300 ease-in-out">
        {getIcon()}
      </div>
      <span className="sr-only">{getLabel()}</span>
    </Button>
  )
}