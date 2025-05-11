from django.db import models
from common.utils import get_uuid4_str

# Create your models here.

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Product(models.Model):
    id = models.CharField(max_length=512, primary_key=True, default=get_uuid4_str)
    name = models.CharField(max_length=512)
    price_in_inr = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = ProductManager()  # Default manager - filters out deleted objects
    all_objects = models.Manager()  # Use this manager to access all objects including deleted ones

    def __str__(self):
        return self.name

    def soft_delete(self):
        self.is_deleted = True
        self.save()