from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime

def send_weekly_email():
    print(f"Sending weekly email notifications at {datetime.now()}...")

def setup_scheduler(app):
    scheduler = BackgroundScheduler()
    
    # Add scheduled task to run every Monday at 8:00 AM
    scheduler.add_job(
        func=send_weekly_email,
        # trigger=CronTrigger(day_of_week="mon", hour=8, minute=0),  # Every Monday at 8:00 AM
        trigger=IntervalTrigger(seconds=10),  # Every 10 seconds
        id="send_weekly_email",
        name="Send weekly email notifications",
        replace_existing=True
    )
    
    scheduler.start()
    return scheduler

