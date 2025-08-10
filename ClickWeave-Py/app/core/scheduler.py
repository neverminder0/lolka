"""
Scheduler - Time-based automation triggers using APScheduler.
"""

import threading
from typing import Optional, Callable, Dict, Any, List
from datetime import datetime, timedelta
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from ..models.models import ScheduleTrigger, Profile


logger = logging.getLogger(__name__)


class AutomationScheduler:
    """
    Manages scheduled automation triggers using APScheduler.
    """
    
    def __init__(self):
        # Configure APScheduler
        jobstores = {
            'default': MemoryJobStore()
        }
        executors = {
            'default': ThreadPoolExecutor(max_workers=5)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 1
        }
        
        self._scheduler = BackgroundScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone='local'
        )
        
        self._running = False
        self._callbacks: Dict[str, Callable] = {}
        self._scheduled_profiles: Dict[str, Profile] = {}
        self._lock = threading.Lock()
    
    def register_callback(self, callback_type: str, callback: Callable) -> None:
        """Register callback for scheduler events (profile_triggered, schedule_error)."""
        with self._lock:
            self._callbacks[callback_type] = callback
    
    def _trigger_callback(self, callback_type: str, data: Any = None) -> None:
        """Trigger registered callback."""
        with self._lock:
            if callback_type in self._callbacks:
                try:
                    self._callbacks[callback_type](data)
                except Exception as e:
                    logger.error(f"Scheduler callback error for {callback_type}: {e}")
    
    def _execute_profile(self, profile_id: str) -> None:
        """Execute a scheduled profile."""
        try:
            profile = self._scheduled_profiles.get(profile_id)
            if profile is None:
                logger.error(f"Scheduled profile not found: {profile_id}")
                return
            
            logger.info(f"Executing scheduled profile: {profile.name}")
            
            # Trigger callback to start the profile
            self._trigger_callback('profile_triggered', {
                'profile_id': profile_id,
                'profile': profile,
                'trigger_time': datetime.now()
            })
            
        except Exception as e:
            logger.error(f"Error executing scheduled profile {profile_id}: {e}")
            self._trigger_callback('schedule_error', {
                'profile_id': profile_id,
                'error': str(e),
                'timestamp': datetime.now()
            })
    
    def _create_trigger(self, schedule_trigger: ScheduleTrigger):
        """Create APScheduler trigger from ScheduleTrigger model."""
        if schedule_trigger.cron_expression:
            # Use CRON expression if provided
            try:
                # Parse CRON expression (minute hour day month day_of_week)
                parts = schedule_trigger.cron_expression.strip().split()
                if len(parts) != 5:
                    raise ValueError("CRON expression must have 5 parts: minute hour day month day_of_week")
                
                minute, hour, day, month, day_of_week = parts
                
                return CronTrigger(
                    minute=minute,
                    hour=hour,
                    day=day,
                    month=month,
                    day_of_week=day_of_week,
                    start_date=schedule_trigger.start_datetime,
                    end_date=schedule_trigger.end_datetime
                )
            except Exception as e:
                logger.error(f"Invalid CRON expression '{schedule_trigger.cron_expression}': {e}")
                raise
        
        elif schedule_trigger.repeat_interval:
            # Use interval trigger for repeating schedules
            return IntervalTrigger(
                seconds=schedule_trigger.repeat_interval.total_seconds(),
                start_date=schedule_trigger.start_datetime,
                end_date=schedule_trigger.end_datetime
            )
        
        else:
            # Single execution at specified time
            return DateTrigger(run_date=schedule_trigger.start_datetime)
    
    def schedule_profile(self, profile: Profile) -> bool:
        """Schedule a profile for automatic execution."""
        if not profile.schedule_trigger or not profile.schedule_trigger.enabled:
            logger.warning(f"Profile {profile.name} has no enabled schedule trigger")
            return False
        
        try:
            schedule_trigger = profile.schedule_trigger
            
            # Validate schedule
            if schedule_trigger.start_datetime <= datetime.now():
                if not schedule_trigger.repeat_interval and not schedule_trigger.cron_expression:
                    logger.warning(f"Profile {profile.name} has start time in the past with no repeat")
                    return False
            
            # Create APScheduler trigger
            trigger = self._create_trigger(schedule_trigger)
            
            # Store profile reference
            self._scheduled_profiles[profile.id] = profile
            
            # Add job to scheduler
            job_id = f"profile_{profile.id}"
            self._scheduler.add_job(
                func=self._execute_profile,
                args=[profile.id],
                trigger=trigger,
                id=job_id,
                name=f"Execute Profile: {profile.name}",
                replace_existing=True
            )
            
            logger.info(f"Scheduled profile '{profile.name}' starting at {schedule_trigger.start_datetime}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to schedule profile {profile.name}: {e}")
            return False
    
    def unschedule_profile(self, profile_id: str) -> bool:
        """Remove a profile from the schedule."""
        try:
            job_id = f"profile_{profile_id}"
            
            # Remove job from scheduler
            try:
                self._scheduler.remove_job(job_id)
                logger.info(f"Unscheduled profile: {profile_id}")
            except Exception:
                # Job might not exist, which is fine
                pass
            
            # Remove profile reference
            if profile_id in self._scheduled_profiles:
                del self._scheduled_profiles[profile_id]
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to unschedule profile {profile_id}: {e}")
            return False
    
    def update_profile_schedule(self, profile: Profile) -> bool:
        """Update an existing profile's schedule."""
        # Remove existing schedule
        self.unschedule_profile(profile.id)
        
        # Add new schedule if enabled
        if profile.schedule_trigger and profile.schedule_trigger.enabled:
            return self.schedule_profile(profile)
        
        return True
    
    def start(self) -> bool:
        """Start the scheduler."""
        if self._running:
            logger.warning("Scheduler is already running")
            return True
        
        try:
            self._scheduler.start()
            self._running = True
            logger.info("Scheduler started")
            return True
        
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop the scheduler."""
        if not self._running:
            return True
        
        try:
            logger.info("Stopping scheduler...")
            self._scheduler.shutdown(wait=True)
            self._running = False
            logger.info("Scheduler stopped")
            return True
        
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")
            return False
    
    def pause_all(self) -> bool:
        """Pause all scheduled jobs."""
        try:
            self._scheduler.pause()
            logger.info("All scheduled jobs paused")
            return True
        except Exception as e:
            logger.error(f"Failed to pause scheduler: {e}")
            return False
    
    def resume_all(self) -> bool:
        """Resume all scheduled jobs."""
        try:
            self._scheduler.resume()
            logger.info("All scheduled jobs resumed")
            return True
        except Exception as e:
            logger.error(f"Failed to resume scheduler: {e}")
            return False
    
    def pause_profile(self, profile_id: str) -> bool:
        """Pause a specific profile's schedule."""
        try:
            job_id = f"profile_{profile_id}"
            self._scheduler.pause_job(job_id)
            logger.info(f"Paused schedule for profile: {profile_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to pause profile schedule {profile_id}: {e}")
            return False
    
    def resume_profile(self, profile_id: str) -> bool:
        """Resume a specific profile's schedule."""
        try:
            job_id = f"profile_{profile_id}"
            self._scheduler.resume_job(job_id)
            logger.info(f"Resumed schedule for profile: {profile_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to resume profile schedule {profile_id}: {e}")
            return False
    
    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return self._running
    
    def get_scheduled_profiles(self) -> Dict[str, Profile]:
        """Get all currently scheduled profiles."""
        return self._scheduled_profiles.copy()
    
    def get_job_info(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a scheduled job."""
        try:
            job_id = f"profile_{profile_id}"
            job = self._scheduler.get_job(job_id)
            
            if job is None:
                return None
            
            return {
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time,
                'trigger': str(job.trigger),
                'func': job.func.__name__,
                'args': job.args,
                'kwargs': job.kwargs,
                'misfire_grace_time': job.misfire_grace_time,
                'max_instances': job.max_instances
            }
        
        except Exception as e:
            logger.error(f"Failed to get job info for {profile_id}: {e}")
            return None
    
    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """Get information about all scheduled jobs."""
        try:
            jobs = []
            for job in self._scheduler.get_jobs():
                jobs.append({
                    'id': job.id,
                    'name': job.name,
                    'next_run_time': job.next_run_time,
                    'trigger': str(job.trigger),
                    'func': job.func.__name__,
                    'args': job.args,
                    'kwargs': job.kwargs
                })
            return jobs
        
        except Exception as e:
            logger.error(f"Failed to get all jobs: {e}")
            return []
    
    def validate_cron_expression(self, cron_expr: str) -> bool:
        """Validate a CRON expression."""
        try:
            parts = cron_expr.strip().split()
            if len(parts) != 5:
                return False
            
            minute, hour, day, month, day_of_week = parts
            
            # Create a test trigger to validate
            CronTrigger(
                minute=minute,
                hour=hour,
                day=day,
                month=month,
                day_of_week=day_of_week
            )
            return True
        
        except Exception:
            return False
    
    def get_next_run_times(self, schedule_trigger: ScheduleTrigger, count: int = 5) -> List[datetime]:
        """Get the next N run times for a schedule trigger."""
        try:
            trigger = self._create_trigger(schedule_trigger)
            
            # Get next run times
            next_times = []
            current_time = datetime.now()
            
            for _ in range(count):
                next_time = trigger.get_next_fire_time(None, current_time)
                if next_time is None:
                    break
                next_times.append(next_time)
                current_time = next_time + timedelta(seconds=1)
            
            return next_times
        
        except Exception as e:
            logger.error(f"Failed to get next run times: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        try:
            all_jobs = self._scheduler.get_jobs()
            running_jobs = [job for job in all_jobs if job.next_run_time is not None]
            
            return {
                'is_running': self._running,
                'total_jobs': len(all_jobs),
                'active_jobs': len(running_jobs),
                'scheduled_profiles': len(self._scheduled_profiles),
                'scheduler_state': self._scheduler.state.name if self._scheduler else 'STOPPED'
            }
        
        except Exception as e:
            logger.error(f"Failed to get scheduler stats: {e}")
            return {
                'is_running': self._running,
                'total_jobs': 0,
                'active_jobs': 0,
                'scheduled_profiles': 0,
                'scheduler_state': 'ERROR'
            }
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        try:
            self.stop()
        except:
            pass