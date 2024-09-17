from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from app.products.models import Product
from app.products.serializers import ProductSerializer
from app.utils.permissions import IsAdminOrReadOnly
from django.core.cache import cache

from app.utils.uniqe_caching import cached_response


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    @extend_schema(
        operation_id="List Products",
        description="Retrieve a list of all products",
        responses={200: ProductSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return cached_response(self, 'list', request, *args, **kwargs)

    @extend_schema(
        operation_id="Retrieve Product",
        description="Retrieve details of a specific product by SKU",
        responses={200: ProductSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return cached_response(self, 'retrieve', request, *args, **kwargs)

    @extend_schema(
        operation_id="Create Product",
        description="Create a new product",
        responses={200: ProductSerializer},
    )
    def perform_create(self, serializer):
        super().perform_create(serializer)
        cache.clear()

    @extend_schema(
        operation_id="Update Product",
        description="Update an existing product",
        responses={200: ProductSerializer},
    )
    def perform_update(self, serializer):
        super().perform_update(serializer)
        cache.clear()

    @extend_schema(
        operation_id="Delete Product",
        description="Delete an existing product",
        responses={200: ProductSerializer},
    )
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        cache.clear()
