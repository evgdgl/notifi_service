from django.db import models
from django.core.validators import RegexValidator

class Sending(models.Model):
    start_timestamp = models.DateTimeField('start_timestamp')
    message_text = models.CharField(max_length=100)
    customer_properties = models.CharField(max_length=100)
    end_timestamp = models.DateTimeField('end_timestamp')
    
    class Meta:
        managed = True
        db_table = 'sendings'
        
class Customers(models.Model):
    phone_number = models.BigIntegerField(default=0,
        validators=[RegexValidator(r'\d{11}$',
            "Phone number must be entered in the format: '99999999999'.")])
    operator_code = models.IntegerField(default=0, 
        validators=[RegexValidator(r'\d{3}$',
            "Mobile code of operator must be entered in the format: '999'.")])
    tag = models.CharField(max_length=100, blank=True)
    t_zone = models.CharField(default=0, max_length=3,
        validators=[RegexValidator(r'[+]+\d{1,2}$',
            "Time zone must be entered in the format: '+12'.")])
    class Meta:
        managed = True
        db_table = 'customers'
        
class Message(models.Model):
    send_timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10)
    sending = models.ForeignKey(Sending, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    
    class Meta:
        managed = True
        db_table = 'message'
