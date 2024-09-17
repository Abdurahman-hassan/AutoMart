from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied

from app.sales.models import SalesOrder
from app.sales.serializers import SalesOrderSerializer
from rest_framework.permissions import IsAuthenticated

from app.utils.uniqe_caching import cached_response

User = get_user_model()


class SalesOrderViewSet(viewsets.ModelViewSet):
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Use select_related to optimize foreign key lookups
        queryset = SalesOrder.objects.select_related('customer', 'product', 'created_by')
        if user.is_staff:
            # If admin, return all orders
            return queryset
        else:
            # For regular users, only return their orders
            return queryset.filter(customer=user)

    @extend_schema(
        operation_id="List Sales Orders",
        description="Retrieve a list of all sales orders",
        responses={200: SalesOrderSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return cached_response(self, request, queryset, self.get_serializer_class(), 'sales_orders')

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        return cached_response(self, request, obj, self.get_serializer_class(), 'sales_order', is_single_object=True)

    def perform_create(self, serializer):
        """
        Automatically assign the customer based on the authenticated user if they are a customer.
        """
        user = self.request.user
        if user.role != User.CUSTOMER:
            raise serializers.ValidationError("Only customers can create sales orders.")
        serializer.save(customer=user, created_by=user)

    def update(self, request, *args, **kwargs):
        """Override update to prevent modifications to SalesOrder."""
        raise MethodNotAllowed("PUT", detail="Sales orders cannot be updated.")

    def partial_update(self, request, *args, **kwargs):
        """Override partial_update to prevent modifications to SalesOrder."""
        raise MethodNotAllowed("PATCH", detail="Sales orders cannot be partially updated.")

    def destroy(self, request, *args, **kwargs):
        """
        Only allow admins to delete sales orders.
        """
        user = self.request.user
        if not user.is_staff:
            raise PermissionDenied("Only admin users can delete sales orders.")
        return super().destroy(request, *args, **kwargs)