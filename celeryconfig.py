# celeryconfig.py
from celery.schedules import crontab

# Broker and Backend URL
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

# List of modules to import when the Celery worker starts.
imports = ('tasks',) # Your tasks.py file

# Define scheduled tasks
beat_schedule = {
    'daily-inactive-user-reminder': {
        'task': 'tasks.send_daily_reminders', # Task to be created in tasks.py
        'schedule': crontab(hour=20, minute=0), # Every day at 8 PM (20:00)
        'args': ()
    },
    'monthly-activity-report': {
        'task': 'tasks.generate_monthly_report', # Task to be created in tasks.py
        'schedule': crontab(day_of_month=1, hour=3, minute=0), # 1st day of every month at 3 AM
        'args': ()
    },
}

timezone = 'Asia/Kolkata' # Or your desired timezone