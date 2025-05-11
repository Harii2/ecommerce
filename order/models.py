from django.db import models
from django.conf import settings
from common.utils import get_uuid4_str # Assuming you want to use your UUID function

class AddressManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class OrderItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Address(models.Model):
    id = models.CharField(max_length=512, primary_key=True, default=get_uuid4_str)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = AddressManager()  # Default manager - filters out deleted objects
    all_objects = models.Manager()  # Use this manager to access all objects including deleted ones
    
    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country} ({self.user.username})"
    
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ['-is_default', '-created_at']
        
    def soft_delete(self):
        self.is_deleted = True
        self.save()

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELED', 'Canceled'),
    ]

    id = models.CharField(max_length=512, primary_key=True, default=get_uuid4_str)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    # You might want to link to a Cart that was converted into this order
    # cart = models.OneToOneField('cart.Cart', on_delete=models.SET_NULL, null=True, blank=True) 
    
    # User details like name and email will be retrieved from the associated User model (user field above)
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='orders')

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Default to 0, can be updated later
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = OrderManager()  # Default manager - filters out deleted objects
    all_objects = models.Manager()  # Use this manager to access all objects including deleted ones

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
        
    def soft_delete(self):
        self.is_deleted = True
        self.save()

class OrderItem(models.Model):
    id = models.CharField(max_length=512, primary_key=True, default=get_uuid4_str)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE) # String reference
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2) # Store the price when the order was made

    is_deleted = models.BooleanField(default=False)
    
    objects = OrderItemManager()  # Default manager - filters out deleted objects
    all_objects = models.Manager()  # Use this manager to access all objects including deleted ones
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id[:8]}"

    @property
    def item_total(self):
        return self.price_at_purchase * self.quantity
        
    def soft_delete(self):
        self.is_deleted = True
        self.save()
