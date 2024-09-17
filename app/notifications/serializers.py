from rest_framework import serializers
from app.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'product', 'message', 'created_at']

    def validate_product(self, value):
        """ Ensure the product exists before creating the notification """
        if not value:
            raise serializers.ValidationError("Product is required for the notification.")
        return value
