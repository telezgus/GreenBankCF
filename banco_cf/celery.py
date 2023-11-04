import os
from celery import Celery
from celery.schedules import crontab
from django.core.management import call_command
from celery.utils.log import get_task_logger



#<-------Config------->

logger = get_task_logger(__name__)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "banco_cf.settings")
app = Celery("banco_cf")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.worker_cancel_long_running_tasks_on_connection_loss = True



#<-------Schedule------->

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Runs send_mail() every minute
    sender.add_periodic_task(60.0, send_mail.s(), name='send_mail_task')
    # Runs retry_defferred() every 20 minutes
    sender.add_periodic_task(20.0 * 60, retry_deferred.s(), name='retry_deferred_task')
    # Runs purge_mail_log() every day at 00:00
    sender.add_periodic_task(crontab(minute=0, hour=0), purge_mail_log.s(), name='purge_mail_log_task')



#<-------Tasks------->

@app.task
def send_mail():
    """Sends all mails in the queue from django-mailling.
    """
    call_command('send_mail')
    
@app.task
def retry_deferred():
    """This will move any deferred mail back into the normal queue,
        so it will be attempted again on the next send_mail from django-mailling.
    """
    call_command('retry_deferred')
    
@app.task
def purge_mail_log():
    """Purges the mail log for entries older than 7 days from django-mailling.
    """
    call_command('purge_mail_log 7')
    

    
