

from django.contrib import admin
from .models import Category, Product, Order

admin.site.register(Category)
admin.site.register(Product)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'product', 'quantity', 'total_cost', 'location', 'delivery_cost', 'product_price')
    list_filter = ('user', 'location')
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('user', 'product', 'quantity', 'total_cost', 'location', 'delivery_cost', 'product_price')
