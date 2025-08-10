"""
Settings Window - Application settings.
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Optional
import logging

from ...models.models import AppSettings


logger = logging.getLogger(__name__)


class SettingsWindow:
    """Window for application settings."""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.window: Optional[ctk.CTkToplevel] = None
        self.settings = app.get_settings()
        
        # Form variables
        self.theme_var = tk.StringVar(value=self.settings.theme)
        self.language_var = tk.StringVar(value=self.settings.language)
        self.failsafe_var = tk.BooleanVar(value=self.settings.failsafe_enabled)
        self.hotkey_start_stop_var = tk.StringVar(value=self.settings.hotkey_start_stop)
        self.hotkey_pause_resume_var = tk.StringVar(value=self.settings.hotkey_pause_resume)
        self.hotkey_emergency_var = tk.StringVar(value=self.settings.hotkey_emergency_stop)
    
    def show(self):
        """Show the settings window."""
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("Settings")
        self.window.geometry("500x600")
        self.window.transient(self.parent)
        self.window.grab_set()
        
        self._create_widgets()
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"500x600+{x}+{y}")
    
    def _create_widgets(self):
        """Create settings widgets."""
        # Main frame
        main_frame = ctk.CTkScrollableFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Appearance
        appearance_frame = ctk.CTkFrame(main_frame)
        appearance_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            appearance_frame,
            text="Appearance",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Theme
        ctk.CTkLabel(appearance_frame, text="Theme:").pack(anchor="w", padx=15)
        theme_menu = ctk.CTkOptionMenu(
            appearance_frame,
            variable=self.theme_var,
            values=["dark", "light", "system"]
        )
        theme_menu.pack(anchor="w", padx=15, pady=(5, 10))
        
        # Language
        ctk.CTkLabel(appearance_frame, text="Language:").pack(anchor="w", padx=15)
        language_menu = ctk.CTkOptionMenu(
            appearance_frame,
            variable=self.language_var,
            values=["en", "ru"]
        )
        language_menu.pack(anchor="w", padx=15, pady=(5, 15))
        
        # Hotkeys
        hotkey_frame = ctk.CTkFrame(main_frame)
        hotkey_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            hotkey_frame,
            text="Global Hotkeys",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Start/Stop
        ctk.CTkLabel(hotkey_frame, text="Start/Stop:").pack(anchor="w", padx=15)
        start_stop_entry = ctk.CTkEntry(
            hotkey_frame,
            textvariable=self.hotkey_start_stop_var,
            width=150
        )
        start_stop_entry.pack(anchor="w", padx=15, pady=(5, 10))
        
        # Pause/Resume
        ctk.CTkLabel(hotkey_frame, text="Pause/Resume:").pack(anchor="w", padx=15)
        pause_resume_entry = ctk.CTkEntry(
            hotkey_frame,
            textvariable=self.hotkey_pause_resume_var,
            width=150
        )
        pause_resume_entry.pack(anchor="w", padx=15, pady=(5, 10))
        
        # Emergency Stop
        ctk.CTkLabel(hotkey_frame, text="Emergency Stop:").pack(anchor="w", padx=15)
        emergency_entry = ctk.CTkEntry(
            hotkey_frame,
            textvariable=self.hotkey_emergency_var,
            width=150
        )
        emergency_entry.pack(anchor="w", padx=15, pady=(5, 15))
        
        # Safety
        safety_frame = ctk.CTkFrame(main_frame)
        safety_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            safety_frame,
            text="Safety",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Failsafe
        failsafe_check = ctk.CTkCheckBox(
            safety_frame,
            text="Enable failsafe (move mouse to corner to stop)",
            variable=self.failsafe_var
        )
        failsafe_check.pack(anchor="w", padx=15, pady=(5, 15))
        
        # Buttons
        button_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        button_frame.pack(side="bottom", fill="x", padx=20, pady=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._cancel
        )
        cancel_btn.pack(side="right", padx=(5, 0))
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save",
            command=self._save
        )
        save_btn.pack(side="right")
    
    def _save(self):
        """Save settings."""
        try:
            # Create new settings
            new_settings = AppSettings(
                theme=self.theme_var.get(),
                language=self.language_var.get(),
                failsafe_enabled=self.failsafe_var.get(),
                hotkey_start_stop=self.hotkey_start_stop_var.get(),
                hotkey_pause_resume=self.hotkey_pause_resume_var.get(),
                hotkey_emergency_stop=self.hotkey_emergency_var.get()
            )
            
            # Update application settings
            if self.app.update_settings(new_settings):
                messagebox.showinfo("Success", "Settings saved successfully!", parent=self.window)
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Failed to save settings.", parent=self.window)
        
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            messagebox.showerror("Error", f"Failed to save settings: {e}", parent=self.window)
    
    def _cancel(self):
        """Cancel settings."""
        self.window.destroy()