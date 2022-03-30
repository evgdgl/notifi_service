from .models import Sending, Customers, Message

from rest_framework import serializers

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customers
        fields = ['url', 'phone_number', 'operator_code', 'tag', 't_zone']


class SendingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sending
        fields = ['url', 'start_timestamp', 'message_text', 'customer_properties', 
            'end_timestamp']


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['url', 'send_timestamp', 'status', 'sending_id', 
            'customer_id']
