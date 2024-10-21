from django.contrib import admin
from .models import Supplier, PurchaseOrder, OrderItem

admin.site.register(Supplier)
admin.site.register(PurchaseOrder)
admin.site.register(OrderItem)
