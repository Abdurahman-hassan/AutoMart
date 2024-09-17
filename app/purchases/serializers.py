from rest_framework import serializers
from app.purchases.models import PurchaseOrder
from app.products.models import Product


class PurchaseOrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'product', 'quantity', 'purchase_date', 'supplier_name', 'created_by']
        read_only_fields = ['created_by']

    def validate_quantity(self, value):
        """ Ensure quantity is a positive number """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_supplier_name(self, value):
        """ Ensure supplier name is not empty """
        if not value:
            raise serializers.ValidationError("Supplier name is required.")
        return value
