from celery import shared_task
from django.core.management import call_command

@shared_task
def generate_daily_report():
    call_command('generate_report')