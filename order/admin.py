from django.contrib import admin
from .models import Order, OrderItem, Address

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product'] # Use raw_id_fields for better performance
    extra = 0 # Usually, you don't add order items manually here once an order is placed

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shipping_address', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'id', 'shipping_address__address_line_1', 'shipping_address__postal_code')
    list_editable = ['status']
    inlines = [OrderItemInline]
    fieldsets = (
        (None, {
            'fields': ('id', 'user', 'status', 'total_amount')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('id', 'created_at', 'updated_at') # Make total_amount editable

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address_line_1', 'city', 'country', 'is_default')
    list_filter = ('is_default', 'country', 'state', 'created_at')
    search_fields = ('user__username', 'address_line_1', 'city', 'postal_code')
    raw_id_fields = ['user']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price_at_purchase')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'product__name')
    raw_id_fields = ['product', 'order']
