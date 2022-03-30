import django
import requests
django.setup()
from django.conf import settings
from django.db.models import Q

from .models import Sending, Customers, Message

from celery import shared_task

from datetime import datetime


@shared_task
def check_sendings():
    for send in (
                  Sending.objects.filter(
                  start_timestamp__lte=datetime.now(),
                  end_timestamp__gte=datetime.now())
                  ):
        for customer in (
                          Customers.objects.filter(
                          Q(operator_code=send.customer_properties) | 
                          Q(tag=send.customer_properties))
                          ):
            if not (
                     Message.objects.filter(
                        sending_id=send.id, customer_id=customer.id, 
                        status='OK').exists()
                    ):
                try:
                    response = requests.post(f'{settings.EXTERNAL_API_URL}{send.id}', 
                    json={'id': send.id, 'phone': customer.phone_number, 
                    'text': send.message_text}, 
                    headers={'Authorization': f'Bearer {settings.EXTERNAL_API_TOKEN}'}
                    )
                    Message.objects.create(status=response.json()['message'], 
                      sending_id=send.id, customer_id=customer.id)
                except Exception as error:
                    Message.objects.create(status=error.agrs[0], 
                      sending_id=send.id, customer_id=customer.id)
                    pass
                
