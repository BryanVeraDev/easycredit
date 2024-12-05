from django.shortcuts import render

from clients.models import Client

from .models import Credit, Payment, InterestRate, ClientCreditProduct
from .serializers import CreditSerializer, PaymentSerializer, InterestRateSerializer, ClientCreditProductSerializer

from django.core.serializers import serialize

from rest_framework import generics, mixins
from rest_framework import routers, serializers, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from utils.permissions import CustomDjangoModelPermissions

class ClientCreditProductViewSet(viewsets.ModelViewSet):
    queryset = ClientCreditProduct.objects.all()
    serializer_class = ClientCreditProductSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    
class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all().order_by('id')
    serializer_class = CreditSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['client', 'status', 'interest_rate', 'application_date', 'start_date', 'end_date']
    search_fields = ['description', 'client__first_name',  'status']
    ordering_fields = ['id', 'total_amount', 'no_installment', 'application_date', 'start_date', 'end_date', 'penalty_rate', 'status']


    @action(detail=False, methods=['get'], url_path='details/(?P<credit_id>[^/.]+)')
    def credits_by_id(self, request, credit_id=None):
        if not Credit.objects.filter(id=credit_id).exists():
            return Response({"error": "Credit not found"}, status=400)
    
        credits = Credit.objects.filter(id=credit_id)
        serializer = self.get_serializer(credits, many=True)
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='clients/(?P<client_id>[^/.]+)')
    def credits_by_client(self, request, client_id=None):
        if not Client.objects.filter(id=client_id).exists():
            return Response({"error": "Client not found"}, status=400)
    
        credits = Credit.objects.filter(client_id=client_id)
        serializer = self.get_serializer(credits, many=True)
        
        return Response(serializer.data)
              
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('id')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    http_method_names = ['get', 'post', 'put', 'patch']

class InterestRateListCreateView(generics.ListCreateAPIView):
    queryset = InterestRate.objects.all().order_by('id')
    serializer_class = InterestRateSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    
