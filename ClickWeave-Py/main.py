#!/usr/bin/env python3
"""
ClickWeave-Py - Cross-platform Auto-clicker Application
Main entry point for the application.
"""

import sys
import os
import logging
from pathlib import Path

# Add app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('clickweave.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if all required dependencies are installed."""
    required_modules = [
        'customtkinter', 'pynput', 'pyautogui', 'keyboard', 
        'pillow', 'mss', 'apscheduler', 'pydantic', 'psutil'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        logger.error(f"Missing required modules: {', '.join(missing_modules)}")
        logger.error("Please install missing dependencies with: pip install -r requirements.txt")
        return False
    
    return True


def check_single_instance():
    """Check if application is already running."""
    try:
        import psutil
        import os
        
        current_pid = os.getpid()
        current_name = "ClickWeave-Py"
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if (proc.info['pid'] != current_pid and 
                    proc.info['name'] and 
                    'python' in proc.info['name'].lower() and
                    proc.info['cmdline'] and
                    any('main.py' in arg for arg in proc.info['cmdline'])):
                    return False
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return True
    except ImportError:
        logger.warning("psutil not available, skipping single instance check")
        return True


def main():
    """Main application entry point."""
    try:
        logger.info("Starting ClickWeave-Py...")
        
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Check single instance
        if not check_single_instance():
            logger.error("ClickWeave-Py is already running!")
            sys.exit(1)
        
        # Import application components after dependency check
        from core.application import ClickWeaveApplication
        from ui.main_window import MainWindow
        
        # Create application instance
        app = ClickWeaveApplication()
        
        # Initialize application
        if not app.initialize():
            logger.error("Failed to initialize application")
            sys.exit(1)
        
        # Create and show main window
        main_window = MainWindow(app)
        main_window.create_window()
        
        logger.info("ClickWeave-Py started successfully")
        
        # Run the application
        main_window.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
    
    finally:
        logger.info("ClickWeave-Py shutting down...")


if __name__ == "__main__":
    main()