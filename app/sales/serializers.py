from rest_framework import serializers

from app.products.models import Product
from app.sales.models import SalesOrder


class SalesOrderSerializer(serializers.ModelSerializer):
    # Allow the product to be referenced by its ID
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SalesOrder
        fields = ['id', 'customer', 'product', 'quantity', 'price', 'sale_date', 'created_by']
        read_only_fields = ['customer', 'created_by', 'sale_date']

    def validate_quantity(self, value):
        """ Ensure quantity is greater than zero and that stock is sufficient """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        if self.instance and value > self.instance.product.stock:
            raise serializers.ValidationError("Insufficient stock available.")
        return value

    def validate_price(self, value):
        """ Ensure price is positive """
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive value.")
        return value
