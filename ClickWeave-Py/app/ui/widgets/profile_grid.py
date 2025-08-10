"""
Profile Grid Widget - Displays profiles in a grid layout.
"""

import customtkinter as ctk
from typing import Optional, Callable, Dict, Any, List
import logging

from ...models.models import Profile


logger = logging.getLogger(__name__)


class ProfileGrid(ctk.CTkScrollableFrame):
    """Grid widget to display and manage automation profiles."""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._callbacks: Dict[str, Callable] = {}
        self._selected_profile: Optional[Profile] = None
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Create initial UI
        self._create_widgets()
        self.refresh_profiles()
    
    def _create_widgets(self):
        """Create the profile grid widgets."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="Automation Profiles",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # New profile button
        new_btn = ctk.CTkButton(
            self,
            text="+ New Profile",
            command=self._on_new_profile
        )
        new_btn.grid(row=1, column=0, pady=(0, 20), sticky="w")
    
    def _on_new_profile(self):
        """Handle new profile button click."""
        if 'new_profile' in self._callbacks:
            self._callbacks['new_profile']()
    
    def refresh_profiles(self):
        """Refresh the profile display."""
        try:
            profiles = self.app.get_all_profiles()
            
            # Clear existing profile widgets (except header and new button)
            for widget in self.winfo_children()[2:]:
                widget.destroy()
            
            # Display profiles
            if not profiles:
                no_profiles = ctk.CTkLabel(
                    self,
                    text="No profiles created yet. Click 'New Profile' to get started!",
                    text_color="gray"
                )
                no_profiles.grid(row=2, column=0, pady=20)
            else:
                for i, profile in enumerate(profiles):
                    self._create_profile_card(profile, i + 2)
        
        except Exception as e:
            logger.error(f"Error refreshing profiles: {e}")
    
    def _create_profile_card(self, profile: Profile, row: int):
        """Create a profile card widget."""
        # Profile frame
        card = ctk.CTkFrame(self)
        card.grid(row=row, column=0, pady=5, sticky="ew", padx=10)
        card.grid_columnconfigure(1, weight=1)
        
        # Profile name
        name_label = ctk.CTkLabel(
            card,
            text=profile.name,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        
        # Status
        status_text = "Running" if profile.is_active else "Stopped"
        status_color = "green" if profile.is_active else "gray"
        status_label = ctk.CTkLabel(
            card,
            text=f"Status: {status_text}",
            text_color=status_color
        )
        status_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)
        
        # Description
        if profile.description:
            desc_label = ctk.CTkLabel(
                card,
                text=profile.description,
                text_color="gray"
            )
            desc_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=2)
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        # Start/Stop button
        if profile.is_active:
            action_btn = ctk.CTkButton(
                btn_frame,
                text="Stop",
                fg_color="red",
                hover_color="darkred",
                command=lambda: self._trigger_callback('profile_stopped', profile)
            )
        else:
            action_btn = ctk.CTkButton(
                btn_frame,
                text="Start",
                fg_color="green",
                hover_color="darkgreen",
                command=lambda: self._trigger_callback('profile_started', profile)
            )
        action_btn.pack(side="left", padx=(0, 5))
        
        # Edit button
        edit_btn = ctk.CTkButton(
            btn_frame,
            text="Edit",
            command=lambda: self._trigger_callback('profile_edited', profile)
        )
        edit_btn.pack(side="left", padx=5)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete",
            fg_color="red",
            hover_color="darkred",
            command=lambda: self._trigger_callback('profile_deleted', profile)
        )
        delete_btn.pack(side="right")
    
    def register_callback(self, event: str, callback: Callable):
        """Register callback for events."""
        self._callbacks[event] = callback
    
    def _trigger_callback(self, event: str, data=None):
        """Trigger registered callback."""
        if event in self._callbacks:
            try:
                self._callbacks[event](data)
            except Exception as e:
                logger.error(f"Callback error for {event}: {e}")
    
    def get_selected_profile(self) -> Optional[Profile]:
        """Get currently selected profile."""
        return self._selected_profile