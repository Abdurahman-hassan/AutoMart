from django.contrib import admin
from app.notifications.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ('product_name', 'formatted_message', 'created_at')
    readonly_fields = ('product', 'message', 'created_at')  # Make fields read-only
    list_filter = ('created_at',)  # Allow filtering by date

    # Disable adding and updating notifications
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow deletion only for admins
        return request.user.is_staff

    # Customize how the product name is displayed
    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = 'Product'

    # Format the message to show the notification in a cleaner way
    def formatted_message(self, obj):
        return f"Stock for {obj.product.sku} is below threshold. {obj.message}"

    formatted_message.short_description = 'Notification Message'


# Register the Notification model with the customized admin
admin.site.register(Notification, NotificationAdmin)
