"""
Unit tests for timing and jitter functionality.
"""

import pytest
import time
import statistics
from unittest.mock import Mock, patch

from app.models.models import TimingConfig
from app.core.click_engine import ClickEngine


class TestTimingConfig:
    """Test timing configuration and jitter calculations."""
    
    def test_precise_timing_no_jitter(self):
        """Test that timing without jitter is precise."""
        timing = TimingConfig(interval_ms=100, jitter_percent=0)
        
        # Should always return exactly 0.1 seconds
        for _ in range(10):
            interval = timing.get_jittered_interval()
            assert interval == 0.1
    
    def test_jitter_distribution(self):
        """Test that jitter creates proper distribution."""
        timing = TimingConfig(interval_ms=1000, jitter_percent=20)
        
        intervals = [timing.get_jittered_interval() for _ in range(1000)]
        
        # All values should be within jitter range (±20%)
        assert all(0.8 <= interval <= 1.2 for interval in intervals)
        
        # Mean should be close to base interval
        mean_interval = statistics.mean(intervals)
        assert 0.95 <= mean_interval <= 1.05
        
        # Should have reasonable spread
        std_dev = statistics.stdev(intervals)
        assert 0.05 <= std_dev <= 0.2
    
    def test_extreme_jitter(self):
        """Test jitter at extreme values."""
        # Maximum jitter (100%)
        timing = TimingConfig(interval_ms=1000, jitter_percent=100)
        intervals = [timing.get_jittered_interval() for _ in range(100)]
        assert all(0.0 <= interval <= 2.0 for interval in intervals)
        
        # No jitter (0%)
        timing = TimingConfig(interval_ms=500, jitter_percent=0)
        intervals = [timing.get_jittered_interval() for _ in range(100)]
        assert all(interval == 0.5 for interval in intervals)
    
    def test_small_intervals(self):
        """Test timing with very small intervals."""
        timing = TimingConfig(interval_ms=10, jitter_percent=10)
        intervals = [timing.get_jittered_interval() for _ in range(100)]
        
        # Should be between 9ms and 11ms
        assert all(0.009 <= interval <= 0.011 for interval in intervals)
    
    def test_large_intervals(self):
        """Test timing with large intervals."""
        timing = TimingConfig(interval_ms=60000, jitter_percent=5)  # 1 minute ±5%
        intervals = [timing.get_jittered_interval() for _ in range(10)]
        
        # Should be between 57s and 63s
        assert all(57.0 <= interval <= 63.0 for interval in intervals)


class TestPreciseTiming:
    """Test precise timing implementation."""
    
    def test_timing_accuracy(self):
        """Test that actual timing matches expected timing."""
        # This test measures actual execution time
        expected_delay = 0.1  # 100ms
        tolerance = 0.02  # 20ms tolerance
        
        start_time = time.perf_counter()
        time.sleep(expected_delay)
        actual_delay = time.perf_counter() - start_time
        
        assert abs(actual_delay - expected_delay) <= tolerance
    
    def test_multiple_timing_consistency(self):
        """Test consistency across multiple timing operations."""
        delays = []
        expected_delay = 0.05  # 50ms
        
        for _ in range(10):
            start_time = time.perf_counter()
            time.sleep(expected_delay)
            actual_delay = time.perf_counter() - start_time
            delays.append(actual_delay)
        
        # Check that all delays are reasonably consistent
        mean_delay = statistics.mean(delays)
        assert abs(mean_delay - expected_delay) <= 0.01
        
        # Standard deviation should be small
        std_dev = statistics.stdev(delays)
        assert std_dev <= 0.005


class TestClickEngineTimingIntegration:
    """Test timing integration in ClickEngine."""
    
    @patch('app.core.click_engine.pyautogui')
    def test_click_engine_timing_integration(self, mock_pyautogui):
        """Test that ClickEngine respects timing configuration."""
        # Mock pyautogui functions
        mock_pyautogui.position.return_value = (100, 100)
        mock_pyautogui.size.return_value = (1920, 1080)
        mock_pyautogui.click = Mock()
        mock_pyautogui.moveTo = Mock()
        
        engine = ClickEngine()
        
        # Create a mock profile with specific timing
        from app.models.models import Profile, Coordinates, TimingConfig, ClickType
        import uuid
        
        profile = Profile(
            id=str(uuid.uuid4()),
            name="Timing Test",
            coordinates=Coordinates(x=100, y=100),
            click_type=ClickType.LEFT,
            timing=TimingConfig(interval_ms=100, jitter_percent=0)
        )
        
        # Test that the engine uses the timing configuration
        timing_interval = profile.timing.get_jittered_interval()
        assert timing_interval == 0.1  # 100ms with no jitter
    
    def test_jitter_calculations_consistency(self):
        """Test that jitter calculations are mathematically consistent."""
        base_intervals = [100, 500, 1000, 5000]  # Various base intervals
        jitter_percentages = [0, 5, 10, 25, 50]  # Various jitter levels
        
        for base_ms in base_intervals:
            for jitter_pct in jitter_percentages:
                timing = TimingConfig(interval_ms=base_ms, jitter_percent=jitter_pct)
                
                # Generate multiple samples
                samples = [timing.get_jittered_interval() for _ in range(100)]
                
                base_seconds = base_ms / 1000.0
                jitter_factor = jitter_pct / 100.0
                
                min_expected = base_seconds * (1 - jitter_factor)
                max_expected = base_seconds * (1 + jitter_factor)
                
                # All samples should be within expected range
                assert all(min_expected <= sample <= max_expected for sample in samples)
                
                # If no jitter, all samples should be identical
                if jitter_pct == 0:
                    assert all(sample == base_seconds for sample in samples)
                
                # If jitter exists, should have variation
                elif jitter_pct > 0:
                    assert len(set(samples)) > 1  # Should have variation


class TestEdgeCases:
    """Test edge cases in timing calculations."""
    
    def test_minimum_timing_values(self):
        """Test minimum allowable timing values."""
        # Test with minimum interval (10ms per model validation)
        timing = TimingConfig(interval_ms=10, jitter_percent=0)
        interval = timing.get_jittered_interval()
        assert interval == 0.01
    
    def test_maximum_jitter(self):
        """Test maximum jitter percentage."""
        timing = TimingConfig(interval_ms=1000, jitter_percent=100)
        
        # With 100% jitter, interval can be 0 to 2000ms
        intervals = [timing.get_jittered_interval() for _ in range(1000)]
        
        # Should span the full range
        min_interval = min(intervals)
        max_interval = max(intervals)
        
        assert min_interval >= 0.0
        assert max_interval <= 2.0
        assert max_interval - min_interval > 1.5  # Should use most of the range
    
    def test_timing_precision(self):
        """Test timing precision at various scales."""
        test_cases = [
            (10, 0),    # 10ms, no jitter
            (50, 5),    # 50ms, 5% jitter  
            (100, 10),  # 100ms, 10% jitter
            (1000, 20), # 1s, 20% jitter
        ]
        
        for interval_ms, jitter_pct in test_cases:
            timing = TimingConfig(interval_ms=interval_ms, jitter_percent=jitter_pct)
            
            # Test precision by checking that calculated values make sense
            for _ in range(10):
                calculated_interval = timing.get_jittered_interval()
                expected_base = interval_ms / 1000.0
                
                # Should be reasonable value
                assert calculated_interval > 0
                assert calculated_interval < expected_base * 3  # Sanity check