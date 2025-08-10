"""
Toolbar Widget - Top toolbar with actions and settings.
"""

import customtkinter as ctk
from typing import Callable, Dict
import logging


logger = logging.getLogger(__name__)


class Toolbar(ctk.CTkFrame):
    """Top toolbar with application actions."""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._callbacks: Dict[str, Callable] = {}
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create toolbar widgets."""
        # App title
        title = ctk.CTkLabel(
            self,
            text="ClickWeave-Py",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(side="left", padx=10)
        
        # Spacer
        spacer = ctk.CTkFrame(self, width=20, fg_color="transparent")
        spacer.pack(side="left", fill="x", expand=True)
        
        # Theme toggle
        theme_btn = ctk.CTkButton(
            self,
            text="🌙 Dark",
            width=80,
            command=self._toggle_theme
        )
        theme_btn.pack(side="right", padx=5)
        
        # Settings button
        settings_btn = ctk.CTkButton(
            self,
            text="⚙️ Settings",
            width=100,
            command=lambda: self._trigger_callback('settings')
        )
        settings_btn.pack(side="right", padx=5)
        
        # About button
        about_btn = ctk.CTkButton(
            self,
            text="ℹ️ About",
            width=80,
            command=lambda: self._trigger_callback('about')
        )
        about_btn.pack(side="right", padx=5)
    
    def _toggle_theme(self):
        """Toggle between light and dark theme."""
        current_mode = ctk.get_appearance_mode()
        new_mode = "light" if current_mode == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        self._trigger_callback('theme_changed', new_mode)
    
    def register_callback(self, event: str, callback: Callable):
        """Register callback for events."""
        self._callbacks[event] = callback
    
    def _trigger_callback(self, event: str, data=None):
        """Trigger registered callback."""
        if event in self._callbacks:
            try:
                self._callbacks[event](data)
            except Exception as e:
                logger.error(f"Toolbar callback error for {event}: {e}")
    
    def update_status(self):
        """Update toolbar status."""
        pass  # Placeholder for status updates