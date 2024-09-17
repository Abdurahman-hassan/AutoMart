from django.contrib.auth import get_user_model
from django.db import models

from app.products.models import Product
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class PurchaseOrder(models.Model):
    # product being restocked
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_orders',
                                verbose_name=_('Product'))
    # quantity purchased
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Purchase Date'))
    # name of the supplier
    supplier_name = models.CharField(max_length=255, verbose_name=_('Supplier Name'))
    # staff member who created the purchase order
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Created by'))

    def __str__(self):
        return f"Restock of {self.product.name}"

    def save(self, *args, **kwargs):
        # Increase stock when a purchase is made
        if not self.pk:  # Only increase stock for new purchases, not when updating
            self.product.increase_stock(self.quantity)
        super(PurchaseOrder, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-purchase_date']
        verbose_name = _('Purchase Order')
        verbose_name_plural = _('Purchase Orders')
