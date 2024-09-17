from django.db import models
from django.utils.translation import gettext_lazy as _
from app.sales.models import SalesOrder
from django.contrib.auth import get_user_model

User = get_user_model()


class Delivery(models.Model):
    sales_order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE, related_name='delivery')
    tracking_number = models.CharField(max_length=100, unique=True)
    carrier = models.CharField(max_length=100)  # e.g., DHL, FedEx
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled')
    ], default='pending')
    estimated_delivery_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    delivery_person = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                        limit_choices_to={'role': 'delivery'},
                                        related_name='deliveries', verbose_name=_('Delivery Person'))
    delivery_notes = models.TextField(blank=True, verbose_name=_('Delivery Notes'))
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                        verbose_name=_('Delivery Cost'))

    def __str__(self):
        return f"Delivery {self.tracking_number} for Order {self.sales_order.id}"

    class Meta:
        ordering = ['-estimated_delivery_date']
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
