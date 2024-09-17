from celery import shared_task
from app.products.models import Product
from app.notifications.models import Notification
from django.utils.translation import gettext_lazy as _

from octos.logging.general import Logger


@shared_task
def check_low_stock():
    """
    Task that checks for products with stock less than a threshold (e.g., 5).
    Creates a notification for each product that has low stock.
    """
    logger = Logger("notifications").get()

    low_stock_threshold = 5
    low_stock_products = Product.objects.filter(stock__lt=low_stock_threshold)

    for product in low_stock_products:
        # Create a notification for each product with low stock
        message = _('Stock for product {} is below {}. Current stock: {}').format(
            product.name, low_stock_threshold, product.stock
        )
        Notification.objects.create(product=product, message=message)

        logger.info(f"Low stock check completed. {low_stock_products.count()} notifications created.")