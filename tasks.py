# tasks.py in your Django app
from celery import shared_task
from .validation_script import ValidationScript

@shared_task
def validate_certificate_task(certificate_id):
    # Call your validation script
    validation_script = ValidationScript()
    validation_script.validate_certificate(certificate_id)
