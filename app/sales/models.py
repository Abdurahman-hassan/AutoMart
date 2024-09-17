from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.products.models import Product

User = get_user_model()


class SalesOrder(models.Model):
    # customer who made the purchase
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_orders',
                                 verbose_name=_('Customer'), db_index=True)
    # product being sold
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales_orders',
                                verbose_name=_('Product'), db_index=True)
    # quantity of the product being sold
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    # sale price of the product
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Sale Price'))
    # sale date
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Sale Date'), db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Created by'))

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"

    def save(self, *args, **kwargs):
        # Reduce stock when the sale is created
        if not self.pk:  # Only reduce stock for new sales, not when updating
            self.product.reduce_stock(self.quantity)
        super(SalesOrder, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-sale_date']
        verbose_name = _('Sales Order')
        verbose_name_plural = _('Sales Orders')

        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['product']),
            models.Index(fields=['sale_date']),
        ]

        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=1), name='quantity_gte_1'),
        ]
