"""
Main Window - Primary application window with CustomTkinter.
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Optional, Callable, Dict, Any
import logging

from .widgets.profile_grid import ProfileGrid
from .widgets.status_bar import StatusBar
from .widgets.toolbar import Toolbar
from ..core.application import ClickWeaveApplication
from ..models.models import AppSettings, Profile


logger = logging.getLogger(__name__)

# Configure CustomTkinter
ctk.set_appearance_mode("dark")  # Default to dark mode
ctk.set_default_color_theme("blue")  # Blue accent color


class MainWindow:
    """
    Main application window using CustomTkinter.
    """
    
    def __init__(self, app: ClickWeaveApplication):
        self.app = app
        self.root: Optional[ctk.CTk] = None
        
        # UI Components
        self.toolbar: Optional[Toolbar] = None
        self.profile_grid: Optional[ProfileGrid] = None
        self.status_bar: Optional[StatusBar] = None
        
        # Window state
        self._window_width = 1200
        self._window_height = 800
        self._min_width = 800
        self._min_height = 600
        
        # Callbacks
        self._callbacks: Dict[str, Callable] = {}
    
    def create_window(self) -> None:
        """Create and configure the main window."""
        self.root = ctk.CTk()
        self.root.title("ClickWeave-Py - Auto-clicker & Macro Tool")
        self.root.geometry(f"{self._window_width}x{self._window_height}")
        self.root.minsize(self._min_width, self._min_height)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("app/assets/icon.ico")
        except:
            pass  # Icon file not found, continue without it
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(1, weight=1)  # Main content area
        self.root.grid_columnconfigure(0, weight=1)
        
        # Apply theme settings
        self._apply_theme_settings()
        
        # Create UI components
        self._create_toolbar()
        self._create_main_content()
        self._create_status_bar()
        
        # Bind window events
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
        self.root.bind("<Configure>", self._on_window_resize)
        
        # Set up periodic UI updates
        self._schedule_ui_update()
        
        logger.info("Main window created successfully")
    
    def _apply_theme_settings(self) -> None:
        """Apply theme settings from application settings."""
        settings = self.app.get_settings()
        
        # Set appearance mode
        if settings.theme == "dark":
            ctk.set_appearance_mode("dark")
        elif settings.theme == "light":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("system")
        
        # Set accent color
        if settings.accent_color:
            ctk.set_default_color_theme("blue")  # We'll customize colors via individual widgets
    
    def _create_toolbar(self) -> None:
        """Create the top toolbar."""
        self.toolbar = Toolbar(self.root, self.app)
        self.toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        # Register toolbar callbacks
        self.toolbar.register_callback('new_profile', self._on_new_profile)
        self.toolbar.register_callback('import_profile', self._on_import_profile)
        self.toolbar.register_callback('export_profile', self._on_export_profile)
        self.toolbar.register_callback('settings', self._on_open_settings)
        self.toolbar.register_callback('about', self._on_show_about)
        self.toolbar.register_callback('theme_changed', self._on_theme_changed)
        self.toolbar.register_callback('language_changed', self._on_language_changed)
    
    def _create_main_content(self) -> None:
        """Create the main content area."""
        # Main content frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Profile grid
        self.profile_grid = ProfileGrid(main_frame, self.app)
        self.profile_grid.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        # Register profile grid callbacks
        self.profile_grid.register_callback('profile_selected', self._on_profile_selected)
        self.profile_grid.register_callback('profile_started', self._on_profile_started)
        self.profile_grid.register_callback('profile_stopped', self._on_profile_stopped)
        self.profile_grid.register_callback('profile_edited', self._on_profile_edited)
        self.profile_grid.register_callback('profile_deleted', self._on_profile_deleted)
        self.profile_grid.register_callback('profile_duplicated', self._on_profile_duplicated)
    
    def _create_status_bar(self) -> None:
        """Create the bottom status bar."""
        self.status_bar = StatusBar(self.root, self.app)
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
    
    def _schedule_ui_update(self) -> None:
        """Schedule periodic UI updates."""
        if self.root:
            self._update_ui()
            # Schedule next update
            update_interval = self.app.get_settings().ui_update_interval_ms
            self.root.after(update_interval, self._schedule_ui_update)
    
    def _update_ui(self) -> None:
        """Update UI components with current application state."""
        try:
            # Update status bar
            if self.status_bar:
                self.status_bar.update_status()
            
            # Update profile grid
            if self.profile_grid:
                self.profile_grid.refresh_profiles()
            
            # Update toolbar
            if self.toolbar:
                self.toolbar.update_status()
        
        except Exception as e:
            logger.error(f"Error updating UI: {e}")
    
    def _on_window_close(self) -> None:
        """Handle window close event."""
        try:
            # Check if automation is running
            if self.app.is_automation_running():
                result = messagebox.askyesno(
                    "Confirm Exit",
                    "Automation is currently running. Stop and exit?",
                    icon="warning"
                )
                if not result:
                    return
            
            # Shutdown application
            self.app.shutdown()
            
            # Destroy window
            if self.root:
                self.root.destroy()
            
            logger.info("Application window closed")
        
        except Exception as e:
            logger.error(f"Error closing window: {e}")
            # Force close
            if self.root:
                self.root.destroy()
    
    def _on_window_resize(self, event) -> None:
        """Handle window resize event."""
        if event.widget == self.root:
            # Update internal size tracking
            self._window_width = self.root.winfo_width()
            self._window_height = self.root.winfo_height()
    
    def _on_new_profile(self) -> None:
        """Handle new profile creation."""
        from .windows.profile_editor import ProfileEditorWindow
        
        # Create new profile
        profile = self.app.create_profile(
            name=f"New Profile {len(self.app.get_all_profiles()) + 1}",
            description="New automation profile"
        )
        
        # Open profile editor
        editor = ProfileEditorWindow(self.root, self.app, profile)
        editor.show()
    
    def _on_import_profile(self) -> None:
        """Handle profile import."""
        from tkinter import filedialog
        import json
        
        try:
            file_path = filedialog.askopenfilename(
                title="Import Profile",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                parent=self.root
            )
            
            if file_path:
                # Load and validate profile
                with open(file_path, 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                
                # Create new profile from imported data
                profile = Profile(**profile_data)
                profile.id = str(uuid.uuid4())  # Generate new ID
                
                # Save profile
                if self.app.save_profile(profile):
                    messagebox.showinfo(
                        "Import Successful",
                        f"Profile '{profile.name}' imported successfully!",
                        parent=self.root
                    )
                    self.profile_grid.refresh_profiles()
                else:
                    messagebox.showerror(
                        "Import Failed",
                        "Failed to save imported profile.",
                        parent=self.root
                    )
        
        except Exception as e:
            logger.error(f"Profile import failed: {e}")
            messagebox.showerror(
                "Import Error",
                f"Failed to import profile: {str(e)}",
                parent=self.root
            )
    
    def _on_export_profile(self) -> None:
        """Handle profile export."""
        from tkinter import filedialog
        
        # Get selected profile
        selected_profile = self.profile_grid.get_selected_profile()
        if not selected_profile:
            messagebox.showwarning(
                "No Profile Selected",
                "Please select a profile to export.",
                parent=self.root
            )
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export Profile",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialvalue=f"{selected_profile.name}.json",
                parent=self.root
            )
            
            if file_path:
                selected_profile.to_json_file(file_path)
                messagebox.showinfo(
                    "Export Successful",
                    f"Profile '{selected_profile.name}' exported successfully!",
                    parent=self.root
                )
        
        except Exception as e:
            logger.error(f"Profile export failed: {e}")
            messagebox.showerror(
                "Export Error",
                f"Failed to export profile: {str(e)}",
                parent=self.root
            )
    
    def _on_open_settings(self) -> None:
        """Handle settings dialog."""
        from .windows.settings_window import SettingsWindow
        
        settings_window = SettingsWindow(self.root, self.app)
        settings_window.show()
    
    def _on_show_about(self) -> None:
        """Show about dialog."""
        about_text = """ClickWeave-Py v1.0.0

A cross-platform auto-clicker and macro automation tool.

Features:
• Global hotkeys for control
• Unlimited click profiles
• Advanced macro sequences
• Pixel color triggers
• Scheduled automation
• Safe and productive automation

Developed for productivity and UI testing purposes.

© 2024 ClickWeave-Py"""
        
        messagebox.showinfo("About ClickWeave-Py", about_text, parent=self.root)
    
    def _on_theme_changed(self, theme: str) -> None:
        """Handle theme change."""
        settings = self.app.get_settings()
        settings.theme = theme
        self.app.update_settings(settings)
        self._apply_theme_settings()
    
    def _on_language_changed(self, language: str) -> None:
        """Handle language change."""
        settings = self.app.get_settings()
        settings.language = language
        self.app.update_settings(settings)
        # TODO: Implement UI text updates
    
    def _on_profile_selected(self, profile: Profile) -> None:
        """Handle profile selection."""
        logger.debug(f"Profile selected: {profile.name}")
    
    def _on_profile_started(self, profile: Profile) -> None:
        """Handle profile start."""
        success = self.app.start_automation(profile.id)
        if not success:
            messagebox.showerror(
                "Start Failed",
                f"Failed to start automation for profile '{profile.name}'.",
                parent=self.root
            )
    
    def _on_profile_stopped(self, profile: Profile) -> None:
        """Handle profile stop."""
        success = self.app.stop_automation()
        if not success:
            messagebox.showerror(
                "Stop Failed",
                "Failed to stop automation.",
                parent=self.root
            )
    
    def _on_profile_edited(self, profile: Profile) -> None:
        """Handle profile edit."""
        from .windows.profile_editor import ProfileEditorWindow
        
        editor = ProfileEditorWindow(self.root, self.app, profile)
        editor.show()
    
    def _on_profile_deleted(self, profile: Profile) -> None:
        """Handle profile deletion."""
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete profile '{profile.name}'?\n\nThis action cannot be undone.",
            icon="warning",
            parent=self.root
        )
        
        if result:
            success = self.app.delete_profile(profile.id)
            if success:
                self.profile_grid.refresh_profiles()
                messagebox.showinfo(
                    "Profile Deleted",
                    f"Profile '{profile.name}' has been deleted.",
                    parent=self.root
                )
            else:
                messagebox.showerror(
                    "Deletion Failed",
                    f"Failed to delete profile '{profile.name}'.",
                    parent=self.root
                )
    
    def _on_profile_duplicated(self, profile: Profile) -> None:
        """Handle profile duplication."""
        try:
            import uuid
            
            # Create duplicate with new ID and name
            new_profile = Profile(**profile.dict())
            new_profile.id = str(uuid.uuid4())
            new_profile.name = f"{profile.name} (Copy)"
            new_profile.is_active = False
            new_profile.is_paused = False
            
            # Save duplicate
            if self.app.save_profile(new_profile):
                self.profile_grid.refresh_profiles()
                messagebox.showinfo(
                    "Profile Duplicated",
                    f"Profile '{new_profile.name}' created successfully!",
                    parent=self.root
                )
            else:
                messagebox.showerror(
                    "Duplication Failed",
                    "Failed to create duplicate profile.",
                    parent=self.root
                )
        
        except Exception as e:
            logger.error(f"Profile duplication failed: {e}")
            messagebox.showerror(
                "Duplication Error",
                f"Failed to duplicate profile: {str(e)}",
                parent=self.root
            )
    
    def register_callback(self, event: str, callback: Callable) -> None:
        """Register callback for window events."""
        self._callbacks[event] = callback
    
    def show(self) -> None:
        """Show the main window."""
        if self.root:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
    
    def hide(self) -> None:
        """Hide the main window."""
        if self.root:
            self.root.withdraw()
    
    def run(self) -> None:
        """Start the main event loop."""
        if self.root:
            logger.info("Starting main UI event loop")
            self.root.mainloop()
    
    def destroy(self) -> None:
        """Destroy the window."""
        if self.root:
            self.root.destroy()
            self.root = None