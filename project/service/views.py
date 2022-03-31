from django.conf import settings
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication

from .models import Sending, Customers, Message
from .serializers import CustomerSerializer, SendingSerializer, MessageSerializer

from itertools import groupby


class CustomersViewSet(viewsets.ModelViewSet):
    """
    
    API endpoint that allows customers to be viewed or edited.
    
    """
    
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class SendingViewSet(viewsets.ModelViewSet):
    
    """
    
    API endpoint that allows sending to be viewed or edited.
    
    """
    
    queryset = Sending.objects.all()
    serializer_class = SendingSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    

class MessageViewSet(viewsets.ModelViewSet):
    
    """
    
    API endpoint that allows sending to be viewed or edited.
    
    """
    
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    

class CommonStatistic(viewsets.ViewSet):
    
    """
    
    API endpoint with information grouped by status about sending - 
    amount, customer properties, message text.
    
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request, format=None):

        messages = (
            Message.objects.annotate(Count('status'))
                .values('status','sending__message_text', 'sending_id',)
                .annotate(amount=Count('sending_id'))
        )
        queryset = []
        def key(key):
            return key['status'] 
        messages = (sorted(messages, key=key))
        for key, value in groupby(messages, key):
            sendings = {'status':key, 'messages': []}
            queryset.append(sendings)
            for data in value:
                del data['status']
                del data['sending_id']
                sendings['messages'].append(data)
        return Response(queryset)


class SendingStatistic(APIView):
    
    """
    
    API endpoint with detail information about messages
    by sending id.
    
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        queryset = Message.objects.filter(sending_id=pk).values(
            'sending__message_text',
            'sending__start_timestamp',
            'sending__end_timestamp',
            'send_timestamp',
            'status',
            'customer__phone_number'
            )
        return Response(queryset)
