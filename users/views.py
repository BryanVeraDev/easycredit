from django.shortcuts import render

# Create your views here.

from .models import User
from .serializers import UserSerializer

from django.core.serializers import serialize

from rest_framework import routers, serializers, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated

from utils.permissions import CustomDjangoModelPermissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
    
