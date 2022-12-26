# Apscheduler library to schedule jobs. 
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# Import functions to be scheduled.
from Scheduler import excel_creator
from Scheduler import mail_creator

# Scheduler function for excel creation.
def excel_service():
    scheduler = BackgroundScheduler()

    # Creating a trigger time.
    trigger = CronTrigger(
        year="*", month="*", day="*", hour="11", minute="15", second="0"
    )

    # Scheduling a job.
    scheduler.add_job(excel_creator.excel_creation, trigger = trigger)
    
    # Starting the scheduler
    scheduler.start()

def email_service():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(
        year="*", month="*", day="*", hour="20", minute="2", second="0"
    )
    scheduler.add_job(mail_creator.mail_creation, trigger = trigger)
    scheduler.start()
