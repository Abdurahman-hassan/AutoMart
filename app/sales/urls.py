from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.sales.views import SalesOrderViewSet

router = DefaultRouter()

router.register(r'sales_orders', SalesOrderViewSet, basename='sales')

urlpatterns = [
    path('', include(router.urls)),
]
