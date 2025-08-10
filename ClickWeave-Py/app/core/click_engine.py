"""
ClickEngine - Core mouse automation engine with precise timing and safety features.
"""

import time
import threading
from typing import Optional, Callable, Dict, Any
import pyautogui
from pynput import mouse
import logging

from ..models.models import (
    Profile, ClickType, Coordinates, TimingConfig, ClickLimits,
    ExecutionLog, ApplicationState
)


logger = logging.getLogger(__name__)


class ClickEngine:
    """
    Core engine for mouse automation with precise timing and safety controls.
    """
    
    def __init__(self):
        self._running = False
        self._paused = False
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        self._current_profile: Optional[Profile] = None
        self._execution_log: Optional[ExecutionLog] = None
        self._click_count = 0
        self._start_time: Optional[float] = None
        self._last_click_time: Optional[float] = None
        self._callbacks: Dict[str, Callable] = {}
        
        # Safety settings
        self._failsafe_enabled = True
        self._failsafe_corner = "top-left"
        
        # Configure pyautogui
        pyautogui.FAILSAFE = False  # We handle failsafe manually
        pyautogui.PAUSE = 0.01  # Minimal pause between pyautogui commands
    
    def set_failsafe(self, enabled: bool, corner: str = "top-left") -> None:
        """Configure failsafe settings."""
        self._failsafe_enabled = enabled
        self._failsafe_corner = corner
    
    def register_callback(self, event: str, callback: Callable) -> None:
        """Register callback for events (started, stopped, paused, resumed, click)."""
        self._callbacks[event] = callback
    
    def _trigger_callback(self, event: str, data: Any = None) -> None:
        """Trigger registered callback."""
        if event in self._callbacks:
            try:
                self._callbacks[event](data)
            except Exception as e:
                logger.error(f"Callback error for {event}: {e}")
    
    def _check_failsafe(self) -> bool:
        """Check if mouse is in failsafe corner."""
        if not self._failsafe_enabled:
            return False
        
        x, y = pyautogui.position()
        screen_width, screen_height = pyautogui.size()
        
        # Define corner regions (50x50 pixels)
        corner_size = 50
        
        if self._failsafe_corner == "top-left":
            return x <= corner_size and y <= corner_size
        elif self._failsafe_corner == "top-right":
            return x >= screen_width - corner_size and y <= corner_size
        elif self._failsafe_corner == "bottom-left":
            return x <= corner_size and y >= screen_height - corner_size
        elif self._failsafe_corner == "bottom-right":
            return x >= screen_width - corner_size and y >= screen_height - corner_size
        
        return False
    
    def _perform_click(self, coordinates: Coordinates, click_type: ClickType) -> bool:
        """Perform a single click operation."""
        try:
            # Move to coordinates if specified
            if coordinates:
                pyautogui.moveTo(coordinates.x, coordinates.y, duration=0.1)
                time.sleep(0.05)  # Small delay after movement
            
            # Perform the click based on type
            if click_type == ClickType.LEFT:
                pyautogui.click(button='left')
            elif click_type == ClickType.RIGHT:
                pyautogui.click(button='right')
            elif click_type == ClickType.MIDDLE:
                pyautogui.click(button='middle')
            elif click_type == ClickType.DOUBLE:
                pyautogui.doubleClick(button='left')
            elif click_type == ClickType.HOLD:
                pyautogui.mouseDown(button='left')
                time.sleep(0.5)  # Hold for 500ms
                pyautogui.mouseUp(button='left')
            
            self._click_count += 1
            self._last_click_time = time.perf_counter()
            
            # Trigger click callback
            self._trigger_callback('click', {
                'coordinates': coordinates,
                'click_type': click_type,
                'click_count': self._click_count
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Click operation failed: {e}")
            return False
    
    def _check_limits(self, profile: Profile) -> bool:
        """Check if execution limits have been reached."""
        if not profile.limits.has_limits():
            return False
        
        # Check click limit
        if profile.limits.max_clicks and self._click_count >= profile.limits.max_clicks:
            logger.info(f"Click limit reached: {self._click_count}")
            return True
        
        # Check duration limit
        if profile.limits.max_duration_seconds and self._start_time:
            elapsed = time.perf_counter() - self._start_time
            if elapsed >= profile.limits.max_duration_seconds:
                logger.info(f"Duration limit reached: {elapsed:.2f}s")
                return True
        
        return False
    
    def _execution_loop(self, profile: Profile) -> None:
        """Main execution loop for clicking automation."""
        logger.info(f"Starting click automation for profile: {profile.name}")
        
        try:
            while not self._stop_event.is_set():
                # Check for pause
                if self._pause_event.is_set():
                    time.sleep(0.1)
                    continue
                
                # Check failsafe
                if self._check_failsafe():
                    logger.warning("Failsafe triggered - stopping automation")
                    self._trigger_callback('stopped', {'reason': 'failsafe'})
                    break
                
                # Check limits
                if self._check_limits(profile):
                    logger.info("Execution limits reached")
                    self._trigger_callback('stopped', {'reason': 'limits_reached'})
                    break
                
                # Perform click
                if profile.coordinates:
                    success = self._perform_click(profile.coordinates, profile.click_type)
                    if not success:
                        logger.error("Click operation failed")
                        break
                
                # Wait for next interval with jitter
                interval = profile.timing.get_jittered_interval()
                
                # Use precise timing with event checking
                end_time = time.perf_counter() + interval
                while time.perf_counter() < end_time:
                    if self._stop_event.is_set():
                        break
                    if self._pause_event.is_set():
                        # Wait until unpaused
                        while self._pause_event.is_set() and not self._stop_event.is_set():
                            time.sleep(0.01)
                        # Recalculate end time after unpause
                        remaining = end_time - time.perf_counter()
                        if remaining > 0:
                            end_time = time.perf_counter() + remaining
                    time.sleep(0.01)  # Small sleep to prevent busy waiting
        
        except Exception as e:
            logger.error(f"Execution loop error: {e}")
            self._trigger_callback('stopped', {'reason': 'error', 'error': str(e)})
        
        finally:
            # Finalize execution log
            if self._execution_log:
                self._execution_log.end_time = time.time()
                self._execution_log.total_clicks = self._click_count
                if self._click_count > 0 and self._start_time:
                    duration = time.perf_counter() - self._start_time
                    self._execution_log.average_interval_ms = (duration / self._click_count) * 1000
            
            logger.info(f"Click automation stopped. Total clicks: {self._click_count}")
    
    def start(self, profile: Profile) -> bool:
        """Start click automation with the given profile."""
        if self._running:
            logger.warning("Click engine is already running")
            return False
        
        try:
            # Reset state
            self._stop_event.clear()
            self._pause_event.clear()
            self._current_profile = profile
            self._click_count = 0
            self._start_time = time.perf_counter()
            
            # Create execution log
            from datetime import datetime
            import uuid
            self._execution_log = ExecutionLog(
                id=str(uuid.uuid4()),
                profile_id=profile.id,
                profile_name=profile.name,
                start_time=datetime.now()
            )
            
            # Start worker thread
            self._worker_thread = threading.Thread(
                target=self._execution_loop,
                args=(profile,),
                daemon=True
            )
            self._worker_thread.start()
            
            self._running = True
            profile.is_active = True
            
            self._trigger_callback('started', profile)
            logger.info(f"Click automation started for profile: {profile.name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to start click automation: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop click automation."""
        if not self._running:
            return True
        
        try:
            logger.info("Stopping click automation...")
            self._stop_event.set()
            
            # Wait for worker thread to finish
            if self._worker_thread and self._worker_thread.is_alive():
                self._worker_thread.join(timeout=2.0)
            
            # Update state
            self._running = False
            self._paused = False
            if self._current_profile:
                self._current_profile.is_active = False
                self._current_profile.is_paused = False
            
            # Finalize execution log
            if self._execution_log:
                self._execution_log.stopped_by = "manual"
            
            self._trigger_callback('stopped', {'reason': 'manual'})
            logger.info("Click automation stopped")
            return True
        
        except Exception as e:
            logger.error(f"Error stopping click automation: {e}")
            return False
    
    def pause(self) -> bool:
        """Pause click automation."""
        if not self._running or self._paused:
            return False
        
        self._pause_event.set()
        self._paused = True
        if self._current_profile:
            self._current_profile.is_paused = True
        
        self._trigger_callback('paused', self._current_profile)
        logger.info("Click automation paused")
        return True
    
    def resume(self) -> bool:
        """Resume click automation."""
        if not self._running or not self._paused:
            return False
        
        self._pause_event.clear()
        self._paused = False
        if self._current_profile:
            self._current_profile.is_paused = False
        
        self._trigger_callback('resumed', self._current_profile)
        logger.info("Click automation resumed")
        return True
    
    def emergency_stop(self) -> bool:
        """Emergency stop - immediate termination."""
        logger.warning("Emergency stop triggered!")
        
        self._stop_event.set()
        self._running = False
        self._paused = False
        
        if self._current_profile:
            self._current_profile.is_active = False
            self._current_profile.is_paused = False
        
        if self._execution_log:
            self._execution_log.stopped_by = "emergency"
        
        self._trigger_callback('stopped', {'reason': 'emergency'})
        return True
    
    @property
    def is_running(self) -> bool:
        """Check if click automation is running."""
        return self._running
    
    @property
    def is_paused(self) -> bool:
        """Check if click automation is paused."""
        return self._paused
    
    @property
    def current_profile(self) -> Optional[Profile]:
        """Get currently active profile."""
        return self._current_profile
    
    @property
    def click_count(self) -> int:
        """Get current click count."""
        return self._click_count
    
    @property
    def execution_log(self) -> Optional[ExecutionLog]:
        """Get current execution log."""
        return self._execution_log
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current execution statistics."""
        stats = {
            'is_running': self._running,
            'is_paused': self._paused,
            'click_count': self._click_count,
            'profile_name': self._current_profile.name if self._current_profile else None,
        }
        
        if self._start_time:
            stats['elapsed_seconds'] = time.perf_counter() - self._start_time
            if self._click_count > 0:
                stats['average_interval_ms'] = (stats['elapsed_seconds'] / self._click_count) * 1000
        
        return stats