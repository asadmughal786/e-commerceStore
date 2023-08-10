from django.db import models
from authusers.models import User
import os

# Create your models here.

class BaseModel(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Category(BaseModel):
    cat = models.Manager()
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    sub_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_name
    
class Product(BaseModel):
    def product_image_path(instance, filename):
        return os.path.join('products', instance.category.name, instance.subcategory.sub_name, instance.name, filename)  # Corrected
    
    prod_image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=None)
    stock = models.PositiveIntegerField(default=0)
    warrenty = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    prod = models.Manager()
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, unique=True, editable=False)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"{self.product.name}_{self.customer.id}"
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number} for {self.product.name} by {self.customer.username}"
