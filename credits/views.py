from django.shortcuts import render

# Create your views here.

from .models import Credit, Payment, InterestRate, ClientCreditProduct
from .serializers import CreditSerializer, PaymentSerializer, InterestRateSerializer, ClientCreditProductSerializer

from django.core.serializers import serialize

from rest_framework import generics
from rest_framework import routers, serializers, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


class ClientCreditProductViewSet(viewsets.ModelViewSet):
    queryset = ClientCreditProduct.objects.all()
    serializer_class = ClientCreditProductSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    @action(detail=False, methods=['get'], url_path='user/(?P<client_id>[^/.]+)')
    def credits_by_user(self, request, client_id=None):
        if not client_id:
            return Response({"error": "Client ID is required"}, status=400)
        
        credits = Credit.objects.filter(client_id=client_id)
        serializer = self.get_serializer(credits, many=True)
        
        return Response(serializer.data)
              
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class InterestRateListCreateView(generics.ListCreateAPIView):
    queryset = InterestRate.objects.all()
    serializer_class = InterestRateSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
