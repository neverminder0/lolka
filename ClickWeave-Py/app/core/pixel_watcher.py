"""
PixelWatcher - Monitor pixel colors for automation triggers.
"""

import time
import threading
from typing import Optional, Callable, Dict, Any, Tuple
import logging
from PIL import ImageGrab
import mss

from ..models.models import (
    PixelTrigger, ColorInfo, ColorCondition, Coordinates
)


logger = logging.getLogger(__name__)


class PixelWatcher:
    """
    Monitors pixel colors and triggers callbacks when conditions are met.
    """
    
    def __init__(self):
        self._running = False
        self._stop_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        self._triggers: Dict[str, PixelTrigger] = {}
        self._callbacks: Dict[str, Callable] = {}
        self._initial_colors: Dict[str, Tuple[int, int, int]] = {}
        
        # Use mss for faster screenshot capture
        self._sct = mss.mss()
    
    def register_callback(self, trigger_id: str, callback: Callable) -> None:
        """Register callback for when a trigger condition is met."""
        self._callbacks[trigger_id] = callback
    
    def add_trigger(self, trigger_id: str, trigger: PixelTrigger) -> None:
        """Add a pixel trigger to monitor."""
        self._triggers[trigger_id] = trigger
        
        # Capture initial color for 'changed' condition
        if trigger.condition == ColorCondition.CHANGED:
            initial_color = self._get_pixel_color(trigger.coordinates)
            if initial_color:
                self._initial_colors[trigger_id] = initial_color
                logger.debug(f"Captured initial color for trigger {trigger_id}: {initial_color}")
    
    def remove_trigger(self, trigger_id: str) -> None:
        """Remove a pixel trigger."""
        if trigger_id in self._triggers:
            del self._triggers[trigger_id]
        if trigger_id in self._callbacks:
            del self._callbacks[trigger_id]
        if trigger_id in self._initial_colors:
            del self._initial_colors[trigger_id]
    
    def clear_triggers(self) -> None:
        """Remove all triggers."""
        self._triggers.clear()
        self._callbacks.clear()
        self._initial_colors.clear()
    
    def _get_pixel_color(self, coordinates: Coordinates) -> Optional[Tuple[int, int, int]]:
        """Get the RGB color of a pixel at the specified coordinates."""
        try:
            # Use mss for faster capture of a single pixel region
            monitor = {
                "top": coordinates.y,
                "left": coordinates.x,
                "width": 1,
                "height": 1
            }
            
            screenshot = self._sct.grab(monitor)
            # Convert to PIL Image and get pixel
            img = screenshot.copy()
            pixel = img.getpixel((0, 0))
            
            # Handle different pixel formats (RGB, RGBA, etc.)
            if len(pixel) >= 3:
                return (pixel[0], pixel[1], pixel[2])
            else:
                logger.warning(f"Unexpected pixel format at ({coordinates.x}, {coordinates.y}): {pixel}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get pixel color at ({coordinates.x}, {coordinates.y}): {e}")
            return None
    
    def _color_matches(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], tolerance: int) -> bool:
        """Check if two colors match within tolerance."""
        r_diff = abs(color1[0] - color2[0])
        g_diff = abs(color1[1] - color2[1])
        b_diff = abs(color1[2] - color2[2])
        
        return r_diff <= tolerance and g_diff <= tolerance and b_diff <= tolerance
    
    def _check_trigger_condition(self, trigger_id: str, trigger: PixelTrigger, current_color: Tuple[int, int, int]) -> bool:
        """Check if a trigger condition is met."""
        target_color = trigger.color.to_rgb_tuple()
        tolerance = trigger.color.tolerance
        
        if trigger.condition == ColorCondition.EXACT:
            return self._color_matches(current_color, target_color, tolerance)
        
        elif trigger.condition == ColorCondition.SIMILAR:
            return self._color_matches(current_color, target_color, tolerance)
        
        elif trigger.condition == ColorCondition.CHANGED:
            initial_color = self._initial_colors.get(trigger_id)
            if initial_color is None:
                logger.warning(f"No initial color stored for trigger {trigger_id}")
                return False
            
            # Check if color has changed from initial
            return not self._color_matches(current_color, initial_color, tolerance)
        
        else:
            logger.error(f"Unknown color condition: {trigger.condition}")
            return False
    
    def _trigger_callback(self, trigger_id: str, trigger: PixelTrigger, current_color: Tuple[int, int, int]) -> None:
        """Trigger callback for a matched condition."""
        if trigger_id in self._callbacks:
            try:
                callback_data = {
                    'trigger_id': trigger_id,
                    'trigger': trigger,
                    'current_color': current_color,
                    'timestamp': time.time()
                }
                self._callbacks[trigger_id](callback_data)
            except Exception as e:
                logger.error(f"Pixel trigger callback error for {trigger_id}: {e}")
    
    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        logger.info("Starting pixel monitoring")
        
        try:
            while not self._stop_event.is_set():
                # Check each active trigger
                for trigger_id, trigger in self._triggers.items():
                    if not trigger.enabled:
                        continue
                    
                    if self._stop_event.is_set():
                        break
                    
                    try:
                        # Get current pixel color
                        current_color = self._get_pixel_color(trigger.coordinates)
                        if current_color is None:
                            continue
                        
                        # Check trigger condition
                        if self._check_trigger_condition(trigger_id, trigger, current_color):
                            logger.debug(f"Trigger condition met for {trigger_id}: {current_color}")
                            self._trigger_callback(trigger_id, trigger, current_color)
                        
                    except Exception as e:
                        logger.error(f"Error checking trigger {trigger_id}: {e}")
                
                # Wait for the check interval
                if self._triggers:
                    # Use the minimum check interval from all triggers
                    min_interval = min(t.check_interval_ms for t in self._triggers.values() if t.enabled)
                    sleep_time = min_interval / 1000.0
                else:
                    sleep_time = 0.1  # Default sleep time when no triggers
                
                # Use event-based waiting for precise timing and quick stop response
                self._stop_event.wait(timeout=sleep_time)
        
        except Exception as e:
            logger.error(f"Pixel monitoring loop error: {e}")
        
        finally:
            logger.info("Pixel monitoring stopped")
    
    def start(self) -> bool:
        """Start pixel monitoring."""
        if self._running:
            logger.warning("Pixel watcher is already running")
            return True
        
        if not self._triggers:
            logger.warning("No pixel triggers to monitor")
            return False
        
        try:
            self._stop_event.clear()
            
            # Start monitoring thread
            self._worker_thread = threading.Thread(
                target=self._monitoring_loop,
                daemon=True
            )
            self._worker_thread.start()
            
            self._running = True
            logger.info("Pixel monitoring started")
            return True
        
        except Exception as e:
            logger.error(f"Failed to start pixel monitoring: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop pixel monitoring."""
        if not self._running:
            return True
        
        try:
            logger.info("Stopping pixel monitoring...")
            self._stop_event.set()
            
            # Wait for worker thread to finish
            if self._worker_thread and self._worker_thread.is_alive():
                self._worker_thread.join(timeout=2.0)
            
            self._running = False
            logger.info("Pixel monitoring stopped")
            return True
        
        except Exception as e:
            logger.error(f"Error stopping pixel monitoring: {e}")
            return False
    
    def is_running(self) -> bool:
        """Check if pixel monitoring is running."""
        return self._running
    
    def get_current_color(self, coordinates: Coordinates) -> Optional[Tuple[int, int, int]]:
        """Get the current color at specified coordinates (utility method)."""
        return self._get_pixel_color(coordinates)
    
    def test_trigger(self, trigger: PixelTrigger) -> Dict[str, Any]:
        """Test a trigger and return current status."""
        current_color = self._get_pixel_color(trigger.coordinates)
        if current_color is None:
            return {
                'success': False,
                'error': 'Failed to capture pixel color'
            }
        
        # Create a temporary trigger ID for testing
        temp_id = "test_trigger"
        if trigger.condition == ColorCondition.CHANGED:
            # For testing, use the target color as initial color
            self._initial_colors[temp_id] = trigger.color.to_rgb_tuple()
        
        condition_met = self._check_trigger_condition(temp_id, trigger, current_color)
        
        # Clean up temporary data
        if temp_id in self._initial_colors:
            del self._initial_colors[temp_id]
        
        return {
            'success': True,
            'current_color': current_color,
            'target_color': trigger.color.to_rgb_tuple(),
            'condition_met': condition_met,
            'tolerance': trigger.color.tolerance,
            'condition': trigger.condition
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current monitoring statistics."""
        active_triggers = sum(1 for t in self._triggers.values() if t.enabled)
        
        return {
            'is_running': self._running,
            'total_triggers': len(self._triggers),
            'active_triggers': active_triggers,
            'trigger_ids': list(self._triggers.keys())
        }
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        try:
            self.stop()
            if hasattr(self, '_sct'):
                self._sct.close()
        except:
            pass