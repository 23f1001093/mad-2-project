from celery.schedules import crontab


broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

#  modules to import when the Celery worker starts.
imports = ('tasks',) 

# scheduled tasks
beat_schedule = {
    'daily-inactive-user-reminder': {
        'task': 'tasks.send_daily_reminders', # Task to be created in tasks.py
        'schedule': crontab(hour=20, minute=0),
        'args': ()
    },
    'monthly-activity-report': {
        'task': 'tasks.generate_monthly_report', 
        'schedule': crontab(day_of_month=1, hour=3, minute=0), # 1st day of every month at 3 AM
        'args': ()
    },
}

timezone = 'Asia/Kolkata' 