"""
Application - Main application class that integrates all core components.
"""

import os
import logging
import threading
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
import json

from .click_engine import ClickEngine
from .macro_engine import MacroEngine
from .hotkey_manager import HotkeyManager
from .pixel_watcher import PixelWatcher
from .scheduler import AutomationScheduler
from ..models.models import (
    Profile, AppSettings, ExecutionLog, ApplicationState,
    TriggerType, HotkeyStatus
)


logger = logging.getLogger(__name__)


class ClickWeaveApplication:
    """
    Main application class that coordinates all automation components.
    """
    
    def __init__(self):
        # Initialize core components
        self.click_engine = ClickEngine()
        self.macro_engine = MacroEngine()
        self.hotkey_manager = HotkeyManager()
        self.pixel_watcher = PixelWatcher()
        self.scheduler = AutomationScheduler()
        
        # Application state
        self._profiles: Dict[str, Profile] = {}
        self._settings: AppSettings = AppSettings()
        self._application_state = ApplicationState()
        self._execution_logs: List[ExecutionLog] = []
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Initialize components
        self._setup_callbacks()
        self._load_settings()
        self._create_data_directories()
    
    def _setup_callbacks(self) -> None:
        """Set up callbacks between components."""
        # Hotkey callbacks
        self.hotkey_manager.register_callback('start_stop', self._on_start_stop_hotkey)
        self.hotkey_manager.register_callback('pause_resume', self._on_pause_resume_hotkey)
        self.hotkey_manager.register_callback('emergency_stop', self._on_emergency_stop_hotkey)
        
        # Engine callbacks
        self.click_engine.register_callback('started', self._on_automation_started)
        self.click_engine.register_callback('stopped', self._on_automation_stopped)
        self.click_engine.register_callback('paused', self._on_automation_paused)
        self.click_engine.register_callback('resumed', self._on_automation_resumed)
        
        self.macro_engine.register_callback('started', self._on_automation_started)
        self.macro_engine.register_callback('stopped', self._on_automation_stopped)
        self.macro_engine.register_callback('paused', self._on_automation_paused)
        self.macro_engine.register_callback('resumed', self._on_automation_resumed)
        
        # Scheduler callbacks
        self.scheduler.register_callback('profile_triggered', self._on_scheduled_profile_triggered)
        self.scheduler.register_callback('schedule_error', self._on_schedule_error)
    
    def _create_data_directories(self) -> None:
        """Create necessary data directories."""
        directories = [
            self._settings.profiles_directory,
            self._settings.logs_directory,
            'app/data'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _load_settings(self) -> None:
        """Load application settings."""
        settings_path = 'app/data/settings.json'
        try:
            self._settings = AppSettings.from_json_file(settings_path)
            logger.info("Settings loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load settings, using defaults: {e}")
            self._settings = AppSettings()
    
    def _save_settings(self) -> None:
        """Save application settings."""
        settings_path = 'app/data/settings.json'
        try:
            self._settings.to_json_file(settings_path)
            logger.debug("Settings saved successfully")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
    
    def _on_start_stop_hotkey(self) -> None:
        """Handle start/stop hotkey."""
        with self._lock:
            if self.is_automation_running():
                self.stop_automation()
            else:
                # Find the last active profile or first available profile
                active_profile = self.get_active_profile()
                if active_profile:
                    self.start_automation(active_profile.id)
    
    def _on_pause_resume_hotkey(self) -> None:
        """Handle pause/resume hotkey."""
        with self._lock:
            if self.is_automation_running():
                if self.is_automation_paused():
                    self.resume_automation()
                else:
                    self.pause_automation()
    
    def _on_emergency_stop_hotkey(self) -> None:
        """Handle emergency stop hotkey."""
        with self._lock:
            self.emergency_stop()
    
    def _on_automation_started(self, profile: Profile) -> None:
        """Handle automation started event."""
        with self._lock:
            self._application_state.is_running = True
            self._application_state.active_profile_id = profile.id
            self._application_state.last_action_time = datetime.now()
            logger.info(f"Automation started: {profile.name}")
    
    def _on_automation_stopped(self, data: Dict[str, Any]) -> None:
        """Handle automation stopped event."""
        with self._lock:
            self._application_state.is_running = False
            self._application_state.active_profile_id = None
            
            # Add execution log
            if hasattr(self.click_engine, 'execution_log') and self.click_engine.execution_log:
                self._add_execution_log(self.click_engine.execution_log)
            elif hasattr(self.macro_engine, 'execution_log') and self.macro_engine.execution_log:
                self._add_execution_log(self.macro_engine.execution_log)
            
            reason = data.get('reason', 'unknown')
            logger.info(f"Automation stopped: {reason}")
    
    def _on_automation_paused(self, profile: Optional[Profile]) -> None:
        """Handle automation paused event."""
        logger.info("Automation paused")
    
    def _on_automation_resumed(self, profile: Optional[Profile]) -> None:
        """Handle automation resumed event."""
        with self._lock:
            self._application_state.last_action_time = datetime.now()
        logger.info("Automation resumed")
    
    def _on_scheduled_profile_triggered(self, data: Dict[str, Any]) -> None:
        """Handle scheduled profile trigger."""
        profile_id = data.get('profile_id')
        if profile_id:
            logger.info(f"Scheduled profile triggered: {profile_id}")
            self.start_automation(profile_id)
    
    def _on_schedule_error(self, data: Dict[str, Any]) -> None:
        """Handle scheduler error."""
        error = data.get('error', 'Unknown error')
        profile_id = data.get('profile_id', 'Unknown')
        logger.error(f"Scheduler error for profile {profile_id}: {error}")
    
    def _add_execution_log(self, log: ExecutionLog) -> None:
        """Add execution log to history."""
        self._execution_logs.append(log)
        
        # Limit log entries
        if len(self._execution_logs) > self._settings.max_log_entries:
            self._execution_logs = self._execution_logs[-self._settings.max_log_entries:]
        
        # Save to CSV
        self._save_execution_log_to_csv(log)
    
    def _save_execution_log_to_csv(self, log: ExecutionLog) -> None:
        """Save execution log to CSV file."""
        try:
            import csv
            from datetime import datetime
            
            csv_path = os.path.join(
                self._settings.logs_directory,
                f"execution_log_{datetime.now().strftime('%Y_%m')}.csv"
            )
            
            # Check if file exists to add header
            file_exists = os.path.exists(csv_path)
            
            with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Add header if new file
                if not file_exists:
                    writer.writerow([
                        'ID', 'Profile Name', 'Start Time', 'End Time', 
                        'Total Clicks', 'Total Steps', 'Average Interval (ms)',
                        'Duration (s)', 'Stopped By', 'Error Message'
                    ])
                
                # Add log entry
                writer.writerow(log.to_csv_row())
        
        except Exception as e:
            logger.error(f"Failed to save execution log to CSV: {e}")
    
    def initialize(self) -> bool:
        """Initialize the application."""
        try:
            logger.info("Initializing ClickWeave application...")
            
            # Load profiles
            self.load_all_profiles()
            
            # Configure safety settings
            self.click_engine.set_failsafe(
                self._settings.failsafe_enabled,
                self._settings.failsafe_corner
            )
            
            # Start scheduler
            self.scheduler.start()
            
            # Register hotkeys
            self.register_hotkeys()
            
            # Update application state
            self._application_state.total_profiles = len(self._profiles)
            self._application_state.hotkey_status = self.hotkey_manager.get_status()
            
            logger.info("ClickWeave application initialized successfully")
            return True
        
        except Exception as e:
            logger.error(f"Failed to initialize application: {e}")
            return False
    
    def shutdown(self) -> None:
        """Shutdown the application."""
        try:
            logger.info("Shutting down ClickWeave application...")
            
            # Stop all automation
            self.emergency_stop()
            
            # Stop components
            self.pixel_watcher.stop()
            self.scheduler.stop()
            
            # Unregister hotkeys
            self.hotkey_manager.unregister_hotkeys()
            
            # Save settings
            self._save_settings()
            
            logger.info("ClickWeave application shutdown complete")
        
        except Exception as e:
            logger.error(f"Error during application shutdown: {e}")
    
    def create_profile(self, name: str, description: str = "") -> Profile:
        """Create a new automation profile."""
        profile = Profile(
            id=str(uuid.uuid4()),
            name=name,
            description=description
        )
        
        with self._lock:
            self._profiles[profile.id] = profile
            self._application_state.total_profiles = len(self._profiles)
        
        self.save_profile(profile)
        logger.info(f"Created new profile: {name}")
        return profile
    
    def save_profile(self, profile: Profile) -> bool:
        """Save a profile to disk."""
        try:
            profile_path = os.path.join(
                self._settings.profiles_directory,
                f"{profile.id}.json"
            )
            profile.to_json_file(profile_path)
            
            with self._lock:
                self._profiles[profile.id] = profile
            
            logger.debug(f"Saved profile: {profile.name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save profile {profile.name}: {e}")
            return False
    
    def load_profile(self, profile_id: str) -> Optional[Profile]:
        """Load a profile from disk."""
        try:
            profile_path = os.path.join(
                self._settings.profiles_directory,
                f"{profile_id}.json"
            )
            
            if not os.path.exists(profile_path):
                logger.warning(f"Profile file not found: {profile_path}")
                return None
            
            profile = Profile.from_json_file(profile_path)
            
            with self._lock:
                self._profiles[profile.id] = profile
            
            return profile
        
        except Exception as e:
            logger.error(f"Failed to load profile {profile_id}: {e}")
            return None
    
    def load_all_profiles(self) -> int:
        """Load all profiles from disk."""
        try:
            profiles_dir = self._settings.profiles_directory
            if not os.path.exists(profiles_dir):
                return 0
            
            loaded_count = 0
            for filename in os.listdir(profiles_dir):
                if filename.endswith('.json'):
                    profile_id = filename[:-5]  # Remove .json extension
                    if self.load_profile(profile_id):
                        loaded_count += 1
            
            with self._lock:
                self._application_state.total_profiles = len(self._profiles)
            
            logger.info(f"Loaded {loaded_count} profiles")
            return loaded_count
        
        except Exception as e:
            logger.error(f"Failed to load profiles: {e}")
            return 0
    
    def delete_profile(self, profile_id: str) -> bool:
        """Delete a profile."""
        try:
            # Stop automation if this profile is running
            if self._application_state.active_profile_id == profile_id:
                self.stop_automation()
            
            # Unschedule if scheduled
            self.scheduler.unschedule_profile(profile_id)
            
            # Remove from memory
            with self._lock:
                if profile_id in self._profiles:
                    del self._profiles[profile_id]
                self._application_state.total_profiles = len(self._profiles)
            
            # Delete file
            profile_path = os.path.join(
                self._settings.profiles_directory,
                f"{profile_id}.json"
            )
            if os.path.exists(profile_path):
                os.remove(profile_path)
            
            logger.info(f"Deleted profile: {profile_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to delete profile {profile_id}: {e}")
            return False
    
    def get_profile(self, profile_id: str) -> Optional[Profile]:
        """Get a profile by ID."""
        return self._profiles.get(profile_id)
    
    def get_all_profiles(self) -> List[Profile]:
        """Get all profiles."""
        return list(self._profiles.values())
    
    def get_active_profile(self) -> Optional[Profile]:
        """Get the currently active profile."""
        if self._application_state.active_profile_id:
            return self._profiles.get(self._application_state.active_profile_id)
        return None
    
    def start_automation(self, profile_id: str) -> bool:
        """Start automation with the specified profile."""
        profile = self.get_profile(profile_id)
        if not profile:
            logger.error(f"Profile not found: {profile_id}")
            return False
        
        if self.is_automation_running():
            logger.warning("Automation is already running")
            return False
        
        try:
            # Start appropriate engine based on profile content
            if profile.macro_steps:
                success = self.macro_engine.start(profile)
            else:
                success = self.click_engine.start(profile)
            
            if success:
                # Set up pixel triggers if configured
                if (profile.trigger_type == TriggerType.PIXEL_COLOR and 
                    profile.pixel_trigger and profile.pixel_trigger.enabled):
                    self.pixel_watcher.add_trigger(profile_id, profile.pixel_trigger)
                    self.pixel_watcher.register_callback(
                        profile_id, 
                        lambda data: self.start_automation(profile_id)
                    )
                    self.pixel_watcher.start()
            
            return success
        
        except Exception as e:
            logger.error(f"Failed to start automation for profile {profile_id}: {e}")
            return False
    
    def stop_automation(self) -> bool:
        """Stop current automation."""
        try:
            success = True
            
            if self.click_engine.is_running:
                success &= self.click_engine.stop()
            
            if self.macro_engine.is_running:
                success &= self.macro_engine.stop()
            
            # Stop pixel watching
            if self.pixel_watcher.is_running():
                self.pixel_watcher.stop()
            
            return success
        
        except Exception as e:
            logger.error(f"Failed to stop automation: {e}")
            return False
    
    def pause_automation(self) -> bool:
        """Pause current automation."""
        try:
            if self.click_engine.is_running:
                return self.click_engine.pause()
            elif self.macro_engine.is_running:
                return self.macro_engine.pause()
            return False
        
        except Exception as e:
            logger.error(f"Failed to pause automation: {e}")
            return False
    
    def resume_automation(self) -> bool:
        """Resume current automation."""
        try:
            if self.click_engine.is_running:
                return self.click_engine.resume()
            elif self.macro_engine.is_running:
                return self.macro_engine.resume()
            return False
        
        except Exception as e:
            logger.error(f"Failed to resume automation: {e}")
            return False
    
    def emergency_stop(self) -> bool:
        """Emergency stop all automation."""
        try:
            success = True
            
            success &= self.click_engine.emergency_stop()
            success &= self.macro_engine.emergency_stop()
            
            if self.pixel_watcher.is_running():
                success &= self.pixel_watcher.stop()
            
            return success
        
        except Exception as e:
            logger.error(f"Failed to emergency stop: {e}")
            return False
    
    def is_automation_running(self) -> bool:
        """Check if any automation is running."""
        return self.click_engine.is_running or self.macro_engine.is_running
    
    def is_automation_paused(self) -> bool:
        """Check if automation is paused."""
        return self.click_engine.is_paused or self.macro_engine.is_paused
    
    def register_hotkeys(self) -> bool:
        """Register global hotkeys."""
        return self.hotkey_manager.register_hotkeys(self._settings)
    
    def unregister_hotkeys(self) -> bool:
        """Unregister global hotkeys."""
        return self.hotkey_manager.unregister_hotkeys()
    
    def update_settings(self, new_settings: AppSettings) -> bool:
        """Update application settings."""
        try:
            # Update hotkeys if they changed
            if (new_settings.hotkey_start_stop != self._settings.hotkey_start_stop or
                new_settings.hotkey_pause_resume != self._settings.hotkey_pause_resume or
                new_settings.hotkey_emergency_stop != self._settings.hotkey_emergency_stop):
                self.hotkey_manager.update_hotkeys(new_settings)
            
            # Update safety settings
            self.click_engine.set_failsafe(
                new_settings.failsafe_enabled,
                new_settings.failsafe_corner
            )
            
            self._settings = new_settings
            self._save_settings()
            
            # Update application state
            self._application_state.hotkey_status = self.hotkey_manager.get_status()
            
            logger.info("Settings updated successfully")
            return True
        
        except Exception as e:
            logger.error(f"Failed to update settings: {e}")
            return False
    
    def get_settings(self) -> AppSettings:
        """Get current application settings."""
        return self._settings
    
    def get_application_state(self) -> ApplicationState:
        """Get current application state."""
        return self._application_state
    
    def get_execution_logs(self) -> List[ExecutionLog]:
        """Get execution log history."""
        return self._execution_logs.copy()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive application statistics."""
        stats = {
            'application': {
                'is_running': self.is_automation_running(),
                'is_paused': self.is_automation_paused(),
                'active_profile_id': self._application_state.active_profile_id,
                'total_profiles': len(self._profiles),
                'hotkeys_registered': self.hotkey_manager.is_registered()
            },
            'click_engine': self.click_engine.get_stats(),
            'macro_engine': self.macro_engine.get_stats(),
            'pixel_watcher': self.pixel_watcher.get_stats(),
            'scheduler': self.scheduler.get_stats()
        }
        
        return stats