from django.shortcuts import render

# Create your views here.

from .models import Product, ProductType
from .serializers import ProductTypeSerializer, ProductSerializer

#from django.http import JsonResponse
from django.core.serializers import serialize

from rest_framework import routers, serializers, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

#from django.http import HttpResponse

#def index(request):
    #products = Product.objects.all()
    #data = serialize('python', products)
    #context = {'products': products}
    #return render(request, 'products/index.html', context)
    #return JsonResponse(data, safe=False)

class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_filters = ['description']
    filterset_fields = ['description']
    search_fields = ['id', 'description']
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
