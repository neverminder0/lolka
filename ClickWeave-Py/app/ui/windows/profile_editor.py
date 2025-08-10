"""
Profile Editor Window - Edit automation profiles.
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Optional
import logging

from ...models.models import Profile, ClickType, Coordinates, TimingConfig


logger = logging.getLogger(__name__)


class ProfileEditorWindow:
    """Window for editing automation profiles."""
    
    def __init__(self, parent, app, profile: Profile):
        self.parent = parent
        self.app = app
        self.profile = profile
        self.window: Optional[ctk.CTkToplevel] = None
        
        # Form variables
        self.name_var = tk.StringVar(value=profile.name)
        self.description_var = tk.StringVar(value=profile.description)
        self.click_type_var = tk.StringVar(value=profile.click_type.value)
        self.x_var = tk.StringVar(value=str(profile.coordinates.x if profile.coordinates else ""))
        self.y_var = tk.StringVar(value=str(profile.coordinates.y if profile.coordinates else ""))
        self.interval_var = tk.StringVar(value=str(profile.timing.interval_ms))
        self.jitter_var = tk.StringVar(value=str(profile.timing.jitter_percent))
    
    def show(self):
        """Show the profile editor window."""
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title(f"Edit Profile: {self.profile.name}")
        self.window.geometry("600x500")
        self.window.transient(self.parent)
        self.window.grab_set()
        
        self._create_widgets()
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"600x500+{x}+{y}")
    
    def _create_widgets(self):
        """Create editor widgets."""
        # Main frame
        main_frame = ctk.CTkScrollableFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Basic settings
        basic_frame = ctk.CTkFrame(main_frame)
        basic_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            basic_frame,
            text="Basic Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Name
        ctk.CTkLabel(basic_frame, text="Profile Name:").pack(anchor="w", padx=15)
        name_entry = ctk.CTkEntry(
            basic_frame,
            textvariable=self.name_var,
            width=300
        )
        name_entry.pack(anchor="w", padx=15, pady=(5, 10))
        
        # Description
        ctk.CTkLabel(basic_frame, text="Description:").pack(anchor="w", padx=15)
        desc_entry = ctk.CTkEntry(
            basic_frame,
            textvariable=self.description_var,
            width=300
        )
        desc_entry.pack(anchor="w", padx=15, pady=(5, 15))
        
        # Click settings
        click_frame = ctk.CTkFrame(main_frame)
        click_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            click_frame,
            text="Click Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Click type
        ctk.CTkLabel(click_frame, text="Click Type:").pack(anchor="w", padx=15)
        click_type_menu = ctk.CTkOptionMenu(
            click_frame,
            variable=self.click_type_var,
            values=[e.value for e in ClickType]
        )
        click_type_menu.pack(anchor="w", padx=15, pady=(5, 10))
        
        # Coordinates
        coord_frame = ctk.CTkFrame(click_frame, fg_color="transparent")
        coord_frame.pack(anchor="w", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(coord_frame, text="Coordinates:").pack(anchor="w")
        
        coord_input_frame = ctk.CTkFrame(coord_frame, fg_color="transparent")
        coord_input_frame.pack(anchor="w", pady=5)
        
        ctk.CTkLabel(coord_input_frame, text="X:").pack(side="left")
        x_entry = ctk.CTkEntry(coord_input_frame, textvariable=self.x_var, width=80)
        x_entry.pack(side="left", padx=(5, 10))
        
        ctk.CTkLabel(coord_input_frame, text="Y:").pack(side="left")
        y_entry = ctk.CTkEntry(coord_input_frame, textvariable=self.y_var, width=80)
        y_entry.pack(side="left", padx=5)
        
        # Pick coordinates button
        pick_btn = ctk.CTkButton(
            coord_input_frame,
            text="Pick Position",
            command=self._pick_coordinates,
            width=100
        )
        pick_btn.pack(side="left", padx=10)
        
        # Timing settings
        timing_frame = ctk.CTkFrame(main_frame)
        timing_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            timing_frame,
            text="Timing Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Interval
        ctk.CTkLabel(timing_frame, text="Interval (ms):").pack(anchor="w", padx=15)
        interval_entry = ctk.CTkEntry(
            timing_frame,
            textvariable=self.interval_var,
            width=150
        )
        interval_entry.pack(anchor="w", padx=15, pady=(5, 10))
        
        # Jitter
        ctk.CTkLabel(timing_frame, text="Jitter (%):").pack(anchor="w", padx=15)
        jitter_entry = ctk.CTkEntry(
            timing_frame,
            textvariable=self.jitter_var,
            width=150
        )
        jitter_entry.pack(anchor="w", padx=15, pady=(5, 15))
        
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
    
    def _pick_coordinates(self):
        """Pick coordinates using mouse."""
        messagebox.showinfo(
            "Pick Coordinates",
            "Move your mouse to the desired position and press SPACE to capture coordinates.\n\nPress ESC to cancel.",
            parent=self.window
        )
        
        # Hide window temporarily
        self.window.withdraw()
        
        try:
            import pyautogui
            import keyboard
            import time
            
            captured = False
            
            def on_key_event(event):
                nonlocal captured
                if event.name == 'space' and event.event_type == keyboard.KEY_DOWN:
                    x, y = pyautogui.position()
                    self.x_var.set(str(x))
                    self.y_var.set(str(y))
                    captured = True
                elif event.name == 'esc' and event.event_type == keyboard.KEY_DOWN:
                    captured = True
            
            keyboard.hook(on_key_event)
            
            # Wait for key press
            while not captured:
                time.sleep(0.1)
            
            keyboard.unhook_all()
            
        except ImportError:
            messagebox.showerror(
                "Error",
                "Required modules not available for coordinate picking.",
                parent=self.parent
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to pick coordinates: {e}",
                parent=self.parent
            )
        finally:
            # Show window again
            self.window.deiconify()
    
    def _save(self):
        """Save profile changes."""
        try:
            # Validate inputs
            if not self.name_var.get().strip():
                messagebox.showerror("Error", "Profile name is required.", parent=self.window)
                return
            
            try:
                x = int(self.x_var.get()) if self.x_var.get() else 0
                y = int(self.y_var.get()) if self.y_var.get() else 0
                interval = int(self.interval_var.get())
                jitter = int(self.jitter_var.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for coordinates, interval, and jitter.", parent=self.window)
                return
            
            # Update profile
            self.profile.name = self.name_var.get().strip()
            self.profile.description = self.description_var.get().strip()
            self.profile.click_type = ClickType(self.click_type_var.get())
            self.profile.coordinates = Coordinates(x=x, y=y)
            self.profile.timing = TimingConfig(interval_ms=interval, jitter_percent=jitter)
            
            # Save to application
            if self.app.save_profile(self.profile):
                messagebox.showinfo("Success", "Profile saved successfully!", parent=self.window)
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Failed to save profile.", parent=self.window)
        
        except Exception as e:
            logger.error(f"Error saving profile: {e}")
            messagebox.showerror("Error", f"Failed to save profile: {e}", parent=self.window)
    
    def _cancel(self):
        """Cancel editing."""
        self.window.destroy()