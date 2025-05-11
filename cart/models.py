from django.db import models
from django.conf import settings
from common.utils import get_uuid4_str

# Create your models here.

class CartManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class CartItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Cart(models.Model):
    id = models.CharField(max_length=512, primary_key=True, default=get_uuid4_str)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True) # For anonymous users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = CartManager()  # Default manager - filters out deleted objects
    all_objects = models.Manager()  # Use this manager to access all objects including deleted ones

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Anonymous Cart ({self.session_key})"
    
    def soft_delete(self):
        self.is_deleted = True
        self.save()

class CartItem(models.Model):
    id = models.CharField(max_length=512, primary_key=True, default=get_uuid4_str)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE) # String reference
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = CartItemManager()  # Default manager - filters out deleted objects
    all_objects = models.Manager()  # Use this manager to access all objects including deleted ones

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart ({self.cart.id[:8]})"
    
    def soft_delete(self):
        self.is_deleted = True
        self.save()
