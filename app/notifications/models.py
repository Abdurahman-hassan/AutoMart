from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.products.models import Product

User = get_user_model()


class Notification(models.Model):
    # Product with low stock
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='notifications',
                                verbose_name=_('Product'))
    message = models.CharField(max_length=255, verbose_name=_('Message'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return f"Notification for {self.product.name}: {self.message}"

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
