from multiprocessing.resource_tracker import register

from django.contrib import admin

from app.products.models import Product

admin.site.register(Product)
