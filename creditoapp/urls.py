"""
URL configuration for creditoapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from products.views import ProductTypeViewSet, ProductViewSet
from credits.views import CreditViewSet, PaymentViewSet, InterestRateListCreateView
from users.views import UserViewSet
from clients.views import ClientViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'product-types', ProductTypeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'credits', CreditViewSet)
router.register(r'payments', PaymentViewSet)
#router.register(r'interest-rates', InterestRateViewSet)
router.register(r'users', UserViewSet)
router.register(r'clients', ClientViewSet)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    #path('products/', include('products.urls')),
    path('admin/', admin.site.urls),
    path('api/interest-rates/', InterestRateListCreateView.as_view(), name='Interest rates'),
]

