from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from app.purchases.models import PurchaseOrder
from app.purchases.serializers import PurchaseOrderSerializer
from rest_framework.permissions import IsAuthenticated
from app.utils.permissions import IsAdminOrStaff
from app.utils.uniqe_caching import cached_response
from rest_framework.response import Response
from rest_framework import status


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Purchase Orders where:
    - Admin or staff users can create, delete, list, and retrieve.
    - Update is not allowed.
    """
    queryset = PurchaseOrder.objects.select_related('product', 'created_by').all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    @extend_schema(
        operation_id="List Purchase Orders",
        description="Retrieve a list of all purchase orders",
        responses={200: PurchaseOrderSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """
        Return a list of all purchase orders.
        """
        return cached_response(self, 'list', request, *args, **kwargs)

    @extend_schema(
        operation_id="Retrieve Purchase Order",
        description="Retrieve a single purchase order",
        responses={200: PurchaseOrderSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single purchase order.
        """
        return cached_response(self, 'retrieve', request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Create a new purchase order and set the created_by field to the current authenticated user.
        """
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Disable the update of purchase orders.
        """
        return Response({"detail": "Update not allowed on purchase orders."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        """
        Disable partial updates of purchase orders.
        """
        return Response({"detail": "Partial update not allowed on purchase orders."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(
        operation_id="Delete Purchase Order",
        description="Delete a purchase order (Admin/Staff only).",
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a purchase order. Only Admin or Staff can delete.
        """
        return super().destroy(request, *args, **kwargs)
