from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    # Stock Keeping Unit, indexed for fast lookups
    sku = models.CharField(max_length=100, unique=True, verbose_name=_('SKU'), db_index=True)
    # indexed for searching and sorting
    name = models.CharField(max_length=255, verbose_name=_('Product Name'), db_index=True)
    description = models.TextField(verbose_name=_('Product Description'), blank=True)
    # indexed for range queries
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Product Price'), db_index=True)
    # stock quantity
    stock = models.PositiveIntegerField(verbose_name=_('Stock Level'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return f"{self.name} (SKU: {self.sku})"

    def reduce_stock(self, quantity):
        """Reduce stock after a sale"""
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
        else:
            raise ValueError("Insufficient stock")

    def increase_stock(self, quantity):
        """Increase stock after a purchase"""
        self.stock += quantity
        self.save()

    class Meta:
        ordering = ['name']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
        ]
