from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app.customers.serializers import CustomerSerializer
from app.utils.permissions import IsOwnerOrReadOnly
from app.utils.uniqe_caching import cached_response

User = get_user_model()


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(role=User.CUSTOMER)

    @extend_schema(
        operation_id="List Customers",
        description="Retrieve a list of all customers",
        responses={200: CustomerSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return cached_response(self, 'list', request, *args, **kwargs)

    @extend_schema(
        operation_id="Retrieve Customer",
        description="Retrieve details of a specific customer by ID",
        responses={200: CustomerSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return cached_response(self, 'retrieve', request, *args, **kwargs)
