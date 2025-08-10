"""
Data models for ClickWeave-Py application using Pydantic for validation and serialization.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Union, Dict, Any, Tuple
from pydantic import BaseModel, Field, validator, root_validator
import json


class ClickType(str, Enum):
    """Types of mouse clicks."""
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    DOUBLE = "double"
    HOLD = "hold"


class MacroStepType(str, Enum):
    """Types of macro steps."""
    CLICK = "click"
    MOVE = "move"
    DELAY = "delay"
    KEY = "key"
    SCROLL = "scroll"


class TriggerType(str, Enum):
    """Types of triggers for automation."""
    MANUAL = "manual"
    PIXEL_COLOR = "pixel_color"
    SCHEDULED = "scheduled"


class ColorCondition(str, Enum):
    """Color matching conditions."""
    EXACT = "exact"
    SIMILAR = "similar"  # Within tolerance
    CHANGED = "changed"  # Color changed from initial


class Coordinates(BaseModel):
    """Screen coordinates with optional relative positioning."""
    x: int = Field(..., description="X coordinate")
    y: int = Field(..., description="Y coordinate")
    relative_to_window: Optional[str] = Field(None, description="Window title for relative positioning")
    
    def __str__(self) -> str:
        rel_info = f" (relative to: {self.relative_to_window})" if self.relative_to_window else ""
        return f"({self.x}, {self.y}){rel_info}"


class ColorInfo(BaseModel):
    """RGB color information with tolerance."""
    r: int = Field(..., ge=0, le=255, description="Red component")
    g: int = Field(..., ge=0, le=255, description="Green component")
    b: int = Field(..., ge=0, le=255, description="Blue component")
    tolerance: int = Field(10, ge=0, le=255, description="Color matching tolerance")
    
    def to_rgb_tuple(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)
    
    def __str__(self) -> str:
        return f"RGB({self.r}, {self.g}, {self.b}) ±{self.tolerance}"


class MacroStep(BaseModel):
    """Individual step in a macro sequence."""
    id: str = Field(..., description="Unique step identifier")
    type: MacroStepType = Field(..., description="Type of macro step")
    enabled: bool = Field(True, description="Whether step is enabled")
    
    # Click/Move specific
    coordinates: Optional[Coordinates] = Field(None, description="Target coordinates")
    click_type: Optional[ClickType] = Field(None, description="Type of click")
    
    # Delay specific
    delay_ms: Optional[int] = Field(None, ge=0, description="Delay in milliseconds")
    
    # Key specific
    key: Optional[str] = Field(None, description="Key to press")
    modifiers: List[str] = Field(default_factory=list, description="Modifier keys (ctrl, alt, shift)")
    
    # Scroll specific
    scroll_direction: Optional[str] = Field(None, description="Scroll direction (up/down)")
    scroll_amount: Optional[int] = Field(None, description="Scroll amount")
    
    # Loop control
    loop_count: int = Field(1, ge=1, description="Number of times to repeat this step")
    
    @validator('click_type')
    def validate_click_type(cls, v, values):
        if values.get('type') == MacroStepType.CLICK and v is None:
            raise ValueError("click_type is required for CLICK steps")
        return v
    
    @validator('coordinates')
    def validate_coordinates(cls, v, values):
        if values.get('type') in [MacroStepType.CLICK, MacroStepType.MOVE] and v is None:
            raise ValueError("coordinates are required for CLICK and MOVE steps")
        return v
    
    @validator('delay_ms')
    def validate_delay(cls, v, values):
        if values.get('type') == MacroStepType.DELAY and v is None:
            raise ValueError("delay_ms is required for DELAY steps")
        return v
    
    @validator('key')
    def validate_key(cls, v, values):
        if values.get('type') == MacroStepType.KEY and v is None:
            raise ValueError("key is required for KEY steps")
        return v


class PixelTrigger(BaseModel):
    """Pixel color-based trigger configuration."""
    enabled: bool = Field(True, description="Whether trigger is enabled")
    coordinates: Coordinates = Field(..., description="Pixel coordinates to monitor")
    color: ColorInfo = Field(..., description="Target color information")
    condition: ColorCondition = Field(ColorCondition.EXACT, description="Color matching condition")
    check_interval_ms: int = Field(100, ge=50, le=5000, description="Check interval in milliseconds")


class ScheduleTrigger(BaseModel):
    """Scheduled trigger configuration."""
    enabled: bool = Field(True, description="Whether trigger is enabled")
    start_datetime: datetime = Field(..., description="When to start")
    repeat_interval: Optional[timedelta] = Field(None, description="Repeat interval")
    cron_expression: Optional[str] = Field(None, description="CRON expression for complex scheduling")
    end_datetime: Optional[datetime] = Field(None, description="When to stop repeating")


class ClickLimits(BaseModel):
    """Limits for click automation."""
    max_clicks: Optional[int] = Field(None, ge=1, description="Maximum number of clicks")
    max_duration_seconds: Optional[int] = Field(None, ge=1, description="Maximum duration in seconds")
    
    def has_limits(self) -> bool:
        return self.max_clicks is not None or self.max_duration_seconds is not None


class TimingConfig(BaseModel):
    """Timing configuration for clicks."""
    interval_ms: int = Field(1000, ge=10, description="Base interval in milliseconds")
    jitter_percent: int = Field(0, ge=0, le=100, description="Timing jitter percentage")
    
    def get_jittered_interval(self) -> float:
        """Calculate interval with jitter applied."""
        import random
        if self.jitter_percent == 0:
            return self.interval_ms / 1000.0
        
        jitter = self.jitter_percent / 100.0
        min_interval = self.interval_ms * (1 - jitter)
        max_interval = self.interval_ms * (1 + jitter)
        return random.uniform(min_interval, max_interval) / 1000.0


class Profile(BaseModel):
    """Complete automation profile configuration."""
    id: str = Field(..., description="Unique profile identifier")
    name: str = Field(..., min_length=1, description="Profile display name")
    description: str = Field("", description="Profile description")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    modified_at: datetime = Field(default_factory=datetime.now, description="Last modification timestamp")
    
    # Basic click configuration
    click_type: ClickType = Field(ClickType.LEFT, description="Primary click type")
    coordinates: Optional[Coordinates] = Field(None, description="Target coordinates")
    
    # Timing
    timing: TimingConfig = Field(default_factory=TimingConfig, description="Timing configuration")
    
    # Limits
    limits: ClickLimits = Field(default_factory=ClickLimits, description="Click limits")
    
    # Macro steps
    macro_steps: List[MacroStep] = Field(default_factory=list, description="Macro sequence steps")
    
    # Triggers
    trigger_type: TriggerType = Field(TriggerType.MANUAL, description="How automation is triggered")
    pixel_trigger: Optional[PixelTrigger] = Field(None, description="Pixel-based trigger")
    schedule_trigger: Optional[ScheduleTrigger] = Field(None, description="Scheduled trigger")
    
    # Execution state
    is_active: bool = Field(False, description="Whether profile is currently running")
    is_paused: bool = Field(False, description="Whether profile is paused")
    
    @validator('modified_at', always=True)
    def update_modified_at(cls, v):
        return datetime.now()
    
    def to_json_file(self, filepath: str) -> None:
        """Save profile to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.dict(), f, indent=2, default=str, ensure_ascii=False)
    
    @classmethod
    def from_json_file(cls, filepath: str) -> 'Profile':
        """Load profile from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)


class ExecutionLog(BaseModel):
    """Log entry for profile execution."""
    id: str = Field(..., description="Unique log entry identifier")
    profile_id: str = Field(..., description="Profile that was executed")
    profile_name: str = Field(..., description="Profile name at time of execution")
    start_time: datetime = Field(..., description="Execution start time")
    end_time: Optional[datetime] = Field(None, description="Execution end time")
    total_clicks: int = Field(0, ge=0, description="Total clicks performed")
    total_steps: int = Field(0, ge=0, description="Total macro steps executed")
    average_interval_ms: Optional[float] = Field(None, description="Average interval between actions")
    stopped_by: str = Field("unknown", description="How execution was stopped")
    error_message: Optional[str] = Field(None, description="Error message if execution failed")
    
    @property
    def duration(self) -> Optional[timedelta]:
        """Calculate execution duration."""
        if self.end_time is None:
            return None
        return self.end_time - self.start_time
    
    def to_csv_row(self) -> List[str]:
        """Convert to CSV row format."""
        duration_str = str(self.duration.total_seconds()) if self.duration else ""
        return [
            self.id,
            self.profile_name,
            self.start_time.isoformat(),
            self.end_time.isoformat() if self.end_time else "",
            str(self.total_clicks),
            str(self.total_steps),
            str(self.average_interval_ms) if self.average_interval_ms else "",
            duration_str,
            self.stopped_by,
            self.error_message or ""
        ]


class AppSettings(BaseModel):
    """Application settings and preferences."""
    # UI preferences
    theme: str = Field("dark", description="UI theme (light/dark)")
    accent_color: str = Field("#1f538d", description="Accent color for UI")
    language: str = Field("en", description="UI language (en/ru)")
    
    # Global hotkeys
    hotkey_start_stop: str = Field("f8", description="Start/Stop hotkey")
    hotkey_pause_resume: str = Field("f7", description="Pause/Resume hotkey")
    hotkey_emergency_stop: str = Field("esc", description="Emergency stop hotkey")
    
    # Safety settings
    failsafe_enabled: bool = Field(True, description="Enable failsafe corner detection")
    failsafe_corner: str = Field("top-left", description="Failsafe corner (top-left, top-right, etc.)")
    single_instance: bool = Field(True, description="Enforce single application instance")
    
    # Paths
    profiles_directory: str = Field("app/data/profiles", description="Directory for profile files")
    logs_directory: str = Field("app/data/logs", description="Directory for log files")
    
    # Performance
    max_log_entries: int = Field(1000, ge=100, description="Maximum log entries to keep")
    ui_update_interval_ms: int = Field(100, ge=50, description="UI update interval")
    
    def to_json_file(self, filepath: str) -> None:
        """Save settings to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def from_json_file(cls, filepath: str) -> 'AppSettings':
        """Load settings from JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls(**data)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default settings if file doesn't exist or is invalid
            return cls()


class HotkeyStatus(BaseModel):
    """Status of global hotkeys."""
    registered: bool = Field(False, description="Whether hotkeys are registered")
    start_stop_active: bool = Field(False, description="Start/Stop hotkey status")
    pause_resume_active: bool = Field(False, description="Pause/Resume hotkey status")
    emergency_stop_active: bool = Field(False, description="Emergency stop hotkey status")
    error_message: Optional[str] = Field(None, description="Error message if registration failed")


class ApplicationState(BaseModel):
    """Current application state."""
    is_running: bool = Field(False, description="Whether any automation is running")
    active_profile_id: Optional[str] = Field(None, description="Currently active profile ID")
    total_profiles: int = Field(0, description="Total number of profiles")
    hotkey_status: HotkeyStatus = Field(default_factory=HotkeyStatus, description="Hotkey registration status")
    last_action_time: Optional[datetime] = Field(None, description="Time of last automated action")