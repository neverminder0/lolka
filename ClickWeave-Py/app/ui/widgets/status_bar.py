"""
Status Bar Widget - Bottom status bar showing application state.
"""

import customtkinter as ctk
import logging


logger = logging.getLogger(__name__)


class StatusBar(ctk.CTkFrame):
    """Bottom status bar showing application status."""
    
    def __init__(self, parent, app):
        super().__init__(parent, height=30)
        self.app = app
        
        self._create_widgets()
        self.update_status()
    
    def _create_widgets(self):
        """Create status bar widgets."""
        # Status text
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10)
        
        # Hotkey status
        self.hotkey_label = ctk.CTkLabel(
            self,
            text="Hotkeys: Disabled",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.hotkey_label.pack(side="right", padx=10)
    
    def update_status(self):
        """Update status bar with current application state."""
        try:
            state = self.app.get_application_state()
            
            # Update main status
            if state.is_running:
                active_profile = self.app.get_active_profile()
                profile_name = active_profile.name if active_profile else "Unknown"
                self.status_label.configure(
                    text=f"Running: {profile_name}",
                    text_color="green"
                )
            else:
                self.status_label.configure(
                    text="Ready",
                    text_color="white"
                )
            
            # Update hotkey status
            if state.hotkey_status.registered:
                hotkey_text = "Hotkeys: F8=Start/Stop, F7=Pause/Resume, Esc=Emergency"
                self.hotkey_label.configure(
                    text=hotkey_text,
                    text_color="green"
                )
            else:
                self.hotkey_label.configure(
                    text="Hotkeys: Disabled",
                    text_color="red"
                )
        
        except Exception as e:
            logger.error(f"Error updating status bar: {e}")
            self.status_label.configure(
                text="Error",
                text_color="red"
            )