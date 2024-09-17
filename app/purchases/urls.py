from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.purchases.views import PurchaseOrderViewSet

router = DefaultRouter()

router.register(r'purchase_orders', PurchaseOrderViewSet, basename='purchase')

urlpatterns = [
    path('', include(router.urls)),
]
