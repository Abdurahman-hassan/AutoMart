from rest_framework import serializers
from app.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'description', 'price', 'stock', 'created_at', 'updated_at']

    def validate_price(self, value):
        """ Ensure price is positive """
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive value.")
        return value

    def validate_stock(self, value):
        """ Ensure stock is non-negative """
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
