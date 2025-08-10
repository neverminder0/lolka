"""
HotkeyManager - Global hotkey handling for automation control.
"""

import threading
from typing import Optional, Callable, Dict, Any
import keyboard
import logging

from ..models.models import AppSettings, HotkeyStatus


logger = logging.getLogger(__name__)


class HotkeyManager:
    """
    Manages global hotkeys for automation control.
    """
    
    def __init__(self):
        self._registered = False
        self._callbacks: Dict[str, Callable] = {}
        self._hotkey_status = HotkeyStatus()
        self._current_settings: Optional[AppSettings] = None
        self._lock = threading.Lock()
    
    def register_callback(self, action: str, callback: Callable) -> None:
        """Register callback for hotkey actions (start_stop, pause_resume, emergency_stop)."""
        with self._lock:
            self._callbacks[action] = callback
    
    def _trigger_callback(self, action: str, data: Any = None) -> None:
        """Trigger registered callback."""
        with self._lock:
            if action in self._callbacks:
                try:
                    self._callbacks[action](data)
                except Exception as e:
                    logger.error(f"Hotkey callback error for {action}: {e}")
    
    def _on_start_stop_hotkey(self) -> None:
        """Handle start/stop hotkey press."""
        logger.debug("Start/Stop hotkey pressed")
        self._trigger_callback('start_stop')
    
    def _on_pause_resume_hotkey(self) -> None:
        """Handle pause/resume hotkey press."""
        logger.debug("Pause/Resume hotkey pressed")
        self._trigger_callback('pause_resume')
    
    def _on_emergency_stop_hotkey(self) -> None:
        """Handle emergency stop hotkey press."""
        logger.warning("Emergency stop hotkey pressed")
        self._trigger_callback('emergency_stop')
    
    def _normalize_hotkey(self, hotkey: str) -> str:
        """Normalize hotkey string for consistent handling."""
        # Convert to lowercase and handle common variations
        hotkey = hotkey.lower().strip()
        
        # Handle special key mappings
        key_mappings = {
            'esc': 'escape',
            'ctrl': 'control',
            'cmd': 'command',
            'win': 'windows',
            'alt': 'alt',
            'shift': 'shift'
        }
        
        # Split by + for combinations
        parts = [part.strip() for part in hotkey.split('+')]
        normalized_parts = []
        
        for part in parts:
            if part in key_mappings:
                normalized_parts.append(key_mappings[part])
            else:
                # Handle function keys
                if part.startswith('f') and part[1:].isdigit():
                    normalized_parts.append(part)
                else:
                    normalized_parts.append(part)
        
        return '+'.join(normalized_parts)
    
    def register_hotkeys(self, settings: AppSettings) -> bool:
        """Register global hotkeys based on settings."""
        if self._registered:
            logger.warning("Hotkeys are already registered")
            return True
        
        try:
            self._current_settings = settings
            
            # Normalize hotkey strings
            start_stop_key = self._normalize_hotkey(settings.hotkey_start_stop)
            pause_resume_key = self._normalize_hotkey(settings.hotkey_pause_resume)
            emergency_stop_key = self._normalize_hotkey(settings.hotkey_emergency_stop)
            
            logger.info(f"Registering hotkeys: Start/Stop={start_stop_key}, Pause/Resume={pause_resume_key}, Emergency={emergency_stop_key}")
            
            # Register start/stop hotkey
            try:
                keyboard.add_hotkey(start_stop_key, self._on_start_stop_hotkey)
                self._hotkey_status.start_stop_active = True
                logger.debug(f"Registered start/stop hotkey: {start_stop_key}")
            except Exception as e:
                logger.error(f"Failed to register start/stop hotkey '{start_stop_key}': {e}")
                self._hotkey_status.start_stop_active = False
            
            # Register pause/resume hotkey
            try:
                keyboard.add_hotkey(pause_resume_key, self._on_pause_resume_hotkey)
                self._hotkey_status.pause_resume_active = True
                logger.debug(f"Registered pause/resume hotkey: {pause_resume_key}")
            except Exception as e:
                logger.error(f"Failed to register pause/resume hotkey '{pause_resume_key}': {e}")
                self._hotkey_status.pause_resume_active = False
            
            # Register emergency stop hotkey
            try:
                keyboard.add_hotkey(emergency_stop_key, self._on_emergency_stop_hotkey)
                self._hotkey_status.emergency_stop_active = True
                logger.debug(f"Registered emergency stop hotkey: {emergency_stop_key}")
            except Exception as e:
                logger.error(f"Failed to register emergency stop hotkey '{emergency_stop_key}': {e}")
                self._hotkey_status.emergency_stop_active = False
            
            # Check if at least one hotkey was registered successfully
            if (self._hotkey_status.start_stop_active or 
                self._hotkey_status.pause_resume_active or 
                self._hotkey_status.emergency_stop_active):
                self._registered = True
                self._hotkey_status.registered = True
                self._hotkey_status.error_message = None
                logger.info("Global hotkeys registered successfully")
                return True
            else:
                self._hotkey_status.registered = False
                self._hotkey_status.error_message = "Failed to register any hotkeys"
                logger.error("Failed to register any global hotkeys")
                return False
        
        except Exception as e:
            logger.error(f"Failed to register hotkeys: {e}")
            self._hotkey_status.registered = False
            self._hotkey_status.error_message = str(e)
            return False
    
    def unregister_hotkeys(self) -> bool:
        """Unregister all global hotkeys."""
        if not self._registered:
            return True
        
        try:
            logger.info("Unregistering global hotkeys")
            
            # Remove all hotkeys
            keyboard.unhook_all_hotkeys()
            
            # Reset status
            self._registered = False
            self._hotkey_status.registered = False
            self._hotkey_status.start_stop_active = False
            self._hotkey_status.pause_resume_active = False
            self._hotkey_status.emergency_stop_active = False
            self._hotkey_status.error_message = None
            
            logger.info("Global hotkeys unregistered successfully")
            return True
        
        except Exception as e:
            logger.error(f"Failed to unregister hotkeys: {e}")
            self._hotkey_status.error_message = str(e)
            return False
    
    def update_hotkeys(self, settings: AppSettings) -> bool:
        """Update hotkeys with new settings."""
        # Unregister current hotkeys
        self.unregister_hotkeys()
        
        # Register with new settings
        return self.register_hotkeys(settings)
    
    def is_registered(self) -> bool:
        """Check if hotkeys are currently registered."""
        return self._registered
    
    def get_status(self) -> HotkeyStatus:
        """Get current hotkey status."""
        return self._hotkey_status.copy()
    
    def test_hotkey(self, hotkey: str) -> bool:
        """Test if a hotkey string is valid."""
        try:
            normalized = self._normalize_hotkey(hotkey)
            
            # Try to register a temporary hotkey
            def dummy_callback():
                pass
            
            keyboard.add_hotkey(normalized, dummy_callback)
            keyboard.remove_hotkey(normalized)
            
            return True
        except Exception as e:
            logger.debug(f"Hotkey test failed for '{hotkey}': {e}")
            return False
    
    def get_pressed_keys(self) -> str:
        """Get currently pressed keys (for hotkey configuration UI)."""
        try:
            # This is a simple implementation - in a real UI, you might want
            # to use a more sophisticated key capture mechanism
            pressed = []
            
            # Check common modifier keys
            if keyboard.is_pressed('ctrl'):
                pressed.append('ctrl')
            if keyboard.is_pressed('alt'):
                pressed.append('alt')
            if keyboard.is_pressed('shift'):
                pressed.append('shift')
            if keyboard.is_pressed('cmd'):
                pressed.append('cmd')
            
            # Note: Getting other keys while they're pressed is more complex
            # and would require a dedicated key capture mode
            
            return '+'.join(pressed) if pressed else ""
        
        except Exception as e:
            logger.error(f"Failed to get pressed keys: {e}")
            return ""
    
    def start_key_capture(self, callback: Callable[[str], None]) -> None:
        """Start capturing key combinations for hotkey configuration."""
        def on_key_event(event):
            if event.event_type == keyboard.KEY_DOWN:
                # Build key combination string
                keys = []
                
                # Check modifiers
                if keyboard.is_pressed('ctrl'):
                    keys.append('ctrl')
                if keyboard.is_pressed('alt'):
                    keys.append('alt')
                if keyboard.is_pressed('shift'):
                    keys.append('shift')
                
                # Add the main key
                key_name = event.name
                if key_name not in ['ctrl', 'alt', 'shift', 'cmd']:
                    keys.append(key_name)
                
                if keys:
                    hotkey_string = '+'.join(keys)
                    callback(hotkey_string)
        
        try:
            keyboard.hook(on_key_event)
        except Exception as e:
            logger.error(f"Failed to start key capture: {e}")
    
    def stop_key_capture(self) -> None:
        """Stop key capture."""
        try:
            keyboard.unhook_all()
            # Re-register hotkeys if they were registered before
            if self._current_settings and self._registered:
                self.register_hotkeys(self._current_settings)
        except Exception as e:
            logger.error(f"Failed to stop key capture: {e}")
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        try:
            self.unregister_hotkeys()
        except:
            pass