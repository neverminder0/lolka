"""
Unit tests for Pydantic models.
"""

import pytest
from datetime import datetime, timedelta
import uuid

from app.models.models import (
    Profile, MacroStep, MacroStepType, ClickType, Coordinates,
    TimingConfig, ClickLimits, ColorInfo, PixelTrigger, ColorCondition,
    ScheduleTrigger, AppSettings, ExecutionLog
)


class TestCoordinates:
    """Test Coordinates model."""
    
    def test_basic_coordinates(self):
        coords = Coordinates(x=100, y=200)
        assert coords.x == 100
        assert coords.y == 200
        assert coords.relative_to_window is None
    
    def test_relative_coordinates(self):
        coords = Coordinates(x=50, y=75, relative_to_window="Test Window")
        assert coords.relative_to_window == "Test Window"
        assert str(coords) == "(50, 75) (relative to: Test Window)"


class TestTimingConfig:
    """Test TimingConfig model."""
    
    def test_default_timing(self):
        timing = TimingConfig()
        assert timing.interval_ms == 1000
        assert timing.jitter_percent == 0
    
    def test_jitter_calculation(self):
        timing = TimingConfig(interval_ms=1000, jitter_percent=10)
        
        # Test multiple iterations to ensure jitter is working
        intervals = [timing.get_jittered_interval() for _ in range(100)]
        
        # All intervals should be between 0.9 and 1.1 seconds
        assert all(0.9 <= interval <= 1.1 for interval in intervals)
        
        # Should have some variation
        assert len(set(intervals)) > 10
    
    def test_no_jitter(self):
        timing = TimingConfig(interval_ms=500, jitter_percent=0)
        interval = timing.get_jittered_interval()
        assert interval == 0.5


class TestClickLimits:
    """Test ClickLimits model."""
    
    def test_no_limits(self):
        limits = ClickLimits()
        assert not limits.has_limits()
    
    def test_click_limit(self):
        limits = ClickLimits(max_clicks=100)
        assert limits.has_limits()
    
    def test_duration_limit(self):
        limits = ClickLimits(max_duration_seconds=60)
        assert limits.has_limits()
    
    def test_both_limits(self):
        limits = ClickLimits(max_clicks=50, max_duration_seconds=30)
        assert limits.has_limits()


class TestColorInfo:
    """Test ColorInfo model."""
    
    def test_color_creation(self):
        color = ColorInfo(r=255, g=128, b=64, tolerance=5)
        assert color.r == 255
        assert color.g == 128
        assert color.b == 64
        assert color.tolerance == 5
    
    def test_color_validation(self):
        # Test valid range
        ColorInfo(r=0, g=255, b=128)
        
        # Test invalid range
        with pytest.raises(ValueError):
            ColorInfo(r=256, g=128, b=64)
        
        with pytest.raises(ValueError):
            ColorInfo(r=-1, g=128, b=64)
    
    def test_rgb_tuple(self):
        color = ColorInfo(r=100, g=150, b=200)
        assert color.to_rgb_tuple() == (100, 150, 200)


class TestMacroStep:
    """Test MacroStep model."""
    
    def test_click_step(self):
        coords = Coordinates(x=100, y=200)
        step = MacroStep(
            id="step1",
            type=MacroStepType.CLICK,
            coordinates=coords,
            click_type=ClickType.LEFT
        )
        assert step.type == MacroStepType.CLICK
        assert step.click_type == ClickType.LEFT
        assert step.enabled is True
    
    def test_delay_step(self):
        step = MacroStep(
            id="step2",
            type=MacroStepType.DELAY,
            delay_ms=500
        )
        assert step.type == MacroStepType.DELAY
        assert step.delay_ms == 500
    
    def test_key_step(self):
        step = MacroStep(
            id="step3",
            type=MacroStepType.KEY,
            key="space",
            modifiers=["ctrl", "shift"]
        )
        assert step.type == MacroStepType.KEY
        assert step.key == "space"
        assert "ctrl" in step.modifiers
        assert "shift" in step.modifiers
    
    def test_validation_errors(self):
        # Click step without coordinates should fail
        with pytest.raises(ValueError):
            MacroStep(
                id="invalid",
                type=MacroStepType.CLICK,
                click_type=ClickType.LEFT
                # Missing coordinates
            )
        
        # Delay step without delay_ms should fail
        with pytest.raises(ValueError):
            MacroStep(
                id="invalid",
                type=MacroStepType.DELAY
                # Missing delay_ms
            )


class TestProfile:
    """Test Profile model."""
    
    def test_basic_profile(self):
        profile = Profile(
            id=str(uuid.uuid4()),
            name="Test Profile",
            description="A test profile"
        )
        assert profile.name == "Test Profile"
        assert profile.description == "A test profile"
        assert isinstance(profile.created_at, datetime)
        assert isinstance(profile.modified_at, datetime)
    
    def test_profile_with_steps(self):
        coords = Coordinates(x=100, y=200)
        step = MacroStep(
            id="step1",
            type=MacroStepType.CLICK,
            coordinates=coords,
            click_type=ClickType.LEFT
        )
        
        profile = Profile(
            id=str(uuid.uuid4()),
            name="Macro Profile",
            macro_steps=[step]
        )
        
        assert len(profile.macro_steps) == 1
        assert profile.macro_steps[0].type == MacroStepType.CLICK
    
    def test_profile_serialization(self):
        """Test profile can be serialized and deserialized."""
        profile = Profile(
            id=str(uuid.uuid4()),
            name="Serialization Test",
            coordinates=Coordinates(x=50, y=100),
            timing=TimingConfig(interval_ms=2000, jitter_percent=5)
        )
        
        # Convert to dict and back
        profile_dict = profile.dict()
        restored_profile = Profile(**profile_dict)
        
        assert restored_profile.name == profile.name
        assert restored_profile.coordinates.x == 50
        assert restored_profile.timing.interval_ms == 2000


class TestExecutionLog:
    """Test ExecutionLog model."""
    
    def test_basic_log(self):
        log = ExecutionLog(
            id=str(uuid.uuid4()),
            profile_id="test-profile",
            profile_name="Test Profile",
            start_time=datetime.now()
        )
        assert log.profile_name == "Test Profile"
        assert log.total_clicks == 0
        assert log.duration is None  # No end time set
    
    def test_completed_log(self):
        start = datetime.now()
        end = start + timedelta(seconds=30)
        
        log = ExecutionLog(
            id=str(uuid.uuid4()),
            profile_id="test-profile",
            profile_name="Test Profile",
            start_time=start,
            end_time=end,
            total_clicks=10
        )
        
        assert log.duration == timedelta(seconds=30)
        assert log.total_clicks == 10
    
    def test_csv_conversion(self):
        log = ExecutionLog(
            id="test-id",
            profile_id="profile-id",
            profile_name="CSV Test",
            start_time=datetime.now(),
            total_clicks=5
        )
        
        csv_row = log.to_csv_row()
        assert isinstance(csv_row, list)
        assert len(csv_row) == 10  # Should have 10 columns
        assert csv_row[1] == "CSV Test"  # Profile name
        assert csv_row[4] == "5"  # Total clicks


class TestAppSettings:
    """Test AppSettings model."""
    
    def test_default_settings(self):
        settings = AppSettings()
        assert settings.theme == "dark"
        assert settings.language == "en"
        assert settings.hotkey_start_stop == "f8"
        assert settings.failsafe_enabled is True
    
    def test_custom_settings(self):
        settings = AppSettings(
            theme="light",
            language="ru",
            hotkey_start_stop="f9"
        )
        assert settings.theme == "light"
        assert settings.language == "ru"
        assert settings.hotkey_start_stop == "f9"


class TestPixelTrigger:
    """Test PixelTrigger model."""
    
    def test_pixel_trigger(self):
        coords = Coordinates(x=100, y=200)
        color = ColorInfo(r=255, g=0, b=0, tolerance=10)
        
        trigger = PixelTrigger(
            coordinates=coords,
            color=color,
            condition=ColorCondition.EXACT,
            check_interval_ms=200
        )
        
        assert trigger.enabled is True
        assert trigger.condition == ColorCondition.EXACT
        assert trigger.check_interval_ms == 200


class TestScheduleTrigger:
    """Test ScheduleTrigger model."""
    
    def test_one_time_trigger(self):
        future_time = datetime.now() + timedelta(hours=1)
        
        trigger = ScheduleTrigger(
            start_datetime=future_time
        )
        
        assert trigger.enabled is True
        assert trigger.repeat_interval is None
        assert trigger.cron_expression is None
    
    def test_repeating_trigger(self):
        future_time = datetime.now() + timedelta(hours=1)
        interval = timedelta(minutes=30)
        
        trigger = ScheduleTrigger(
            start_datetime=future_time,
            repeat_interval=interval
        )
        
        assert trigger.repeat_interval == interval
    
    def test_cron_trigger(self):
        future_time = datetime.now() + timedelta(hours=1)
        
        trigger = ScheduleTrigger(
            start_datetime=future_time,
            cron_expression="0 9 * * 1-5"  # Weekdays at 9 AM
        )
        
        assert trigger.cron_expression == "0 9 * * 1-5"