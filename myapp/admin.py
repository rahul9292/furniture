from django.contrib import admin
from .models import Product
from .models import Order

# Register the Product model
admin.site.register(Product)
admin.site.register(Order)



