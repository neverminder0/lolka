"""
MacroEngine - Advanced macro automation with support for complex sequences.
"""

import time
import threading
from typing import Optional, Callable, Dict, Any, List
import pyautogui
from pynput import keyboard
import logging

from ..models.models import (
    Profile, MacroStep, MacroStepType, ClickType, Coordinates,
    ExecutionLog
)


logger = logging.getLogger(__name__)


class MacroEngine:
    """
    Advanced macro engine for executing complex automation sequences.
    """
    
    def __init__(self):
        self._running = False
        self._paused = False
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        self._current_profile: Optional[Profile] = None
        self._execution_log: Optional[ExecutionLog] = None
        self._step_count = 0
        self._start_time: Optional[float] = None
        self._callbacks: Dict[str, Callable] = {}
        
        # Configure pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.01
    
    def register_callback(self, event: str, callback: Callable) -> None:
        """Register callback for events (started, stopped, paused, resumed, step_executed)."""
        self._callbacks[event] = callback
    
    def _trigger_callback(self, event: str, data: Any = None) -> None:
        """Trigger registered callback."""
        if event in self._callbacks:
            try:
                self._callbacks[event](data)
            except Exception as e:
                logger.error(f"Callback error for {event}: {e}")
    
    def _execute_click_step(self, step: MacroStep) -> bool:
        """Execute a click macro step."""
        try:
            if not step.coordinates:
                logger.error("Click step missing coordinates")
                return False
            
            # Move to coordinates
            pyautogui.moveTo(step.coordinates.x, step.coordinates.y, duration=0.1)
            time.sleep(0.05)
            
            # Perform click based on type
            if step.click_type == ClickType.LEFT:
                pyautogui.click(button='left')
            elif step.click_type == ClickType.RIGHT:
                pyautogui.click(button='right')
            elif step.click_type == ClickType.MIDDLE:
                pyautogui.click(button='middle')
            elif step.click_type == ClickType.DOUBLE:
                pyautogui.doubleClick(button='left')
            elif step.click_type == ClickType.HOLD:
                pyautogui.mouseDown(button='left')
                time.sleep(0.5)
                pyautogui.mouseUp(button='left')
            
            logger.debug(f"Executed click: {step.click_type} at ({step.coordinates.x}, {step.coordinates.y})")
            return True
            
        except Exception as e:
            logger.error(f"Click step execution failed: {e}")
            return False
    
    def _execute_move_step(self, step: MacroStep) -> bool:
        """Execute a move macro step."""
        try:
            if not step.coordinates:
                logger.error("Move step missing coordinates")
                return False
            
            pyautogui.moveTo(step.coordinates.x, step.coordinates.y, duration=0.2)
            logger.debug(f"Moved to ({step.coordinates.x}, {step.coordinates.y})")
            return True
            
        except Exception as e:
            logger.error(f"Move step execution failed: {e}")
            return False
    
    def _execute_delay_step(self, step: MacroStep) -> bool:
        """Execute a delay macro step."""
        try:
            if step.delay_ms is None:
                logger.error("Delay step missing delay_ms")
                return False
            
            delay_seconds = step.delay_ms / 1000.0
            
            # Use precise timing with event checking
            end_time = time.perf_counter() + delay_seconds
            while time.perf_counter() < end_time:
                if self._stop_event.is_set():
                    return False
                if self._pause_event.is_set():
                    # Wait until unpaused
                    while self._pause_event.is_set() and not self._stop_event.is_set():
                        time.sleep(0.01)
                    # Recalculate end time after unpause
                    remaining = end_time - time.perf_counter()
                    if remaining > 0:
                        end_time = time.perf_counter() + remaining
                time.sleep(0.01)
            
            logger.debug(f"Delayed for {step.delay_ms}ms")
            return True
            
        except Exception as e:
            logger.error(f"Delay step execution failed: {e}")
            return False
    
    def _execute_key_step(self, step: MacroStep) -> bool:
        """Execute a key press macro step."""
        try:
            if not step.key:
                logger.error("Key step missing key")
                return False
            
            # Handle modifiers
            modifiers_pressed = []
            for modifier in step.modifiers:
                mod_key = modifier.lower()
                if mod_key in ['ctrl', 'control']:
                    pyautogui.keyDown('ctrl')
                    modifiers_pressed.append('ctrl')
                elif mod_key in ['alt']:
                    pyautogui.keyDown('alt')
                    modifiers_pressed.append('alt')
                elif mod_key in ['shift']:
                    pyautogui.keyDown('shift')
                    modifiers_pressed.append('shift')
                elif mod_key in ['cmd', 'command', 'win', 'windows']:
                    pyautogui.keyDown('cmd')
                    modifiers_pressed.append('cmd')
            
            # Press the main key
            pyautogui.press(step.key)
            
            # Release modifiers in reverse order
            for modifier in reversed(modifiers_pressed):
                pyautogui.keyUp(modifier)
            
            logger.debug(f"Executed key press: {'+'.join(step.modifiers + [step.key])}")
            return True
            
        except Exception as e:
            logger.error(f"Key step execution failed: {e}")
            return False
    
    def _execute_scroll_step(self, step: MacroStep) -> bool:
        """Execute a scroll macro step."""
        try:
            if not step.scroll_direction or step.scroll_amount is None:
                logger.error("Scroll step missing direction or amount")
                return False
            
            # Get current mouse position for scrolling
            x, y = pyautogui.position()
            
            if step.scroll_direction.lower() == 'up':
                pyautogui.scroll(step.scroll_amount, x=x, y=y)
            elif step.scroll_direction.lower() == 'down':
                pyautogui.scroll(-step.scroll_amount, x=x, y=y)
            else:
                logger.error(f"Invalid scroll direction: {step.scroll_direction}")
                return False
            
            logger.debug(f"Scrolled {step.scroll_direction} by {step.scroll_amount}")
            return True
            
        except Exception as e:
            logger.error(f"Scroll step execution failed: {e}")
            return False
    
    def _execute_macro_step(self, step: MacroStep) -> bool:
        """Execute a single macro step."""
        if not step.enabled:
            logger.debug(f"Skipping disabled step: {step.id}")
            return True
        
        # Execute the step based on its type
        success = False
        if step.type == MacroStepType.CLICK:
            success = self._execute_click_step(step)
        elif step.type == MacroStepType.MOVE:
            success = self._execute_move_step(step)
        elif step.type == MacroStepType.DELAY:
            success = self._execute_delay_step(step)
        elif step.type == MacroStepType.KEY:
            success = self._execute_key_step(step)
        elif step.type == MacroStepType.SCROLL:
            success = self._execute_scroll_step(step)
        else:
            logger.error(f"Unknown step type: {step.type}")
            return False
        
        if success:
            self._step_count += 1
            self._trigger_callback('step_executed', {
                'step': step,
                'step_count': self._step_count
            })
        
        return success
    
    def _execute_macro_sequence(self, steps: List[MacroStep]) -> bool:
        """Execute a sequence of macro steps."""
        try:
            for step in steps:
                if self._stop_event.is_set():
                    logger.info("Macro execution stopped by user")
                    return False
                
                # Wait for unpause
                while self._pause_event.is_set() and not self._stop_event.is_set():
                    time.sleep(0.01)
                
                if self._stop_event.is_set():
                    return False
                
                # Execute step multiple times if loop_count > 1
                for loop_iteration in range(step.loop_count):
                    if self._stop_event.is_set():
                        return False
                    
                    while self._pause_event.is_set() and not self._stop_event.is_set():
                        time.sleep(0.01)
                    
                    if self._stop_event.is_set():
                        return False
                    
                    success = self._execute_macro_step(step)
                    if not success:
                        logger.error(f"Macro step execution failed: {step.id}")
                        return False
                    
                    # Small delay between loop iterations
                    if loop_iteration < step.loop_count - 1:
                        time.sleep(0.05)
            
            return True
            
        except Exception as e:
            logger.error(f"Macro sequence execution failed: {e}")
            return False
    
    def _execution_loop(self, profile: Profile) -> None:
        """Main execution loop for macro automation."""
        logger.info(f"Starting macro automation for profile: {profile.name}")
        
        try:
            if not profile.macro_steps:
                logger.warning("Profile has no macro steps to execute")
                return
            
            # Execute macro sequence once
            success = self._execute_macro_sequence(profile.macro_steps)
            
            if success:
                logger.info("Macro sequence completed successfully")
                self._trigger_callback('stopped', {'reason': 'completed'})
            else:
                logger.error("Macro sequence execution failed")
                self._trigger_callback('stopped', {'reason': 'error'})
        
        except Exception as e:
            logger.error(f"Execution loop error: {e}")
            self._trigger_callback('stopped', {'reason': 'error', 'error': str(e)})
        
        finally:
            # Finalize execution log
            if self._execution_log:
                from datetime import datetime
                self._execution_log.end_time = datetime.now()
                self._execution_log.total_steps = self._step_count
                if self._step_count > 0 and self._start_time:
                    duration = time.perf_counter() - self._start_time
                    self._execution_log.average_interval_ms = (duration / self._step_count) * 1000
            
            logger.info(f"Macro automation stopped. Total steps: {self._step_count}")
    
    def start(self, profile: Profile) -> bool:
        """Start macro automation with the given profile."""
        if self._running:
            logger.warning("Macro engine is already running")
            return False
        
        if not profile.macro_steps:
            logger.error("Cannot start macro automation: no macro steps defined")
            return False
        
        try:
            # Reset state
            self._stop_event.clear()
            self._pause_event.clear()
            self._current_profile = profile
            self._step_count = 0
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
            logger.info(f"Macro automation started for profile: {profile.name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to start macro automation: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop macro automation."""
        if not self._running:
            return True
        
        try:
            logger.info("Stopping macro automation...")
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
            logger.info("Macro automation stopped")
            return True
        
        except Exception as e:
            logger.error(f"Error stopping macro automation: {e}")
            return False
    
    def pause(self) -> bool:
        """Pause macro automation."""
        if not self._running or self._paused:
            return False
        
        self._pause_event.set()
        self._paused = True
        if self._current_profile:
            self._current_profile.is_paused = True
        
        self._trigger_callback('paused', self._current_profile)
        logger.info("Macro automation paused")
        return True
    
    def resume(self) -> bool:
        """Resume macro automation."""
        if not self._running or not self._paused:
            return False
        
        self._pause_event.clear()
        self._paused = False
        if self._current_profile:
            self._current_profile.is_paused = False
        
        self._trigger_callback('resumed', self._current_profile)
        logger.info("Macro automation resumed")
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
        """Check if macro automation is running."""
        return self._running
    
    @property
    def is_paused(self) -> bool:
        """Check if macro automation is paused."""
        return self._paused
    
    @property
    def current_profile(self) -> Optional[Profile]:
        """Get currently active profile."""
        return self._current_profile
    
    @property
    def step_count(self) -> int:
        """Get current step count."""
        return self._step_count
    
    @property
    def execution_log(self) -> Optional[ExecutionLog]:
        """Get current execution log."""
        return self._execution_log
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current execution statistics."""
        stats = {
            'is_running': self._running,
            'is_paused': self._paused,
            'step_count': self._step_count,
            'profile_name': self._current_profile.name if self._current_profile else None,
        }
        
        if self._start_time:
            stats['elapsed_seconds'] = time.perf_counter() - self._start_time
            if self._step_count > 0:
                stats['average_step_interval_ms'] = (stats['elapsed_seconds'] / self._step_count) * 1000
        
        return stats