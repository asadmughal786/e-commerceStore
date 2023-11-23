from django.db import models 
from django.db.models import Count
from authusers.models import User
from shortuuid.django_fields import ShortUUIDField
# import os
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models, IntegrityError
from django.db.models import F
from django.db.models.constraints import UniqueConstraint, CheckConstraint




# Create your models here.


CHOICES = (
    ('Process', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
)

STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('publish', 'Published'),
)

RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)


class BaseModel(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    
    cid = ShortUUIDField(unique=True, length=10, max_length=30,
                        prefix='cat', alphabet='abcdef12345')
    image = models.ImageField(upload_to='Category Images', null=True)
    # cat = models.Manager()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        print('\n\nActual Image size conversion--->>> ', img.size)

        # Resize the image as needed
        output_size = (200, 200)  # Set your desired size
        img = img.resize(output_size)
        print('Image size : --->>>',img.size)
        img.save(self.image.path)
        
# ------------------------------------ Product --------------------------


class Product(BaseModel):
    prod_image = models.ImageField(upload_to='Products', null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None)

    pid = ShortUUIDField(unique=True, length=10, max_length=30,
                        prefix='scat', alphabet='abcdef12345')
    title = models.CharField(max_length=100, default='New Product')
    specification = RichTextUploadingField(
        null=True, blank=True, default='No description')
    description = RichTextUploadingField(max_length=500, blank=True)

    qty = models.PositiveIntegerField(default=0)
    warrenty = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00)
    old_price = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00, blank=True)

    product_status = models.CharField(
        choices=STATUS, max_length=10, default='in_review')

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)

    sku = ShortUUIDField(unique=True, length=4, max_length=20,
                        prefix='sku', alphabet='1234567890')
    date = models.DateTimeField(auto_now_add=True) 

    # prod = models.Manager()

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title

    def get_percentage(self):
        return (self.price/self.old_price) * 100
    
    # Resizing the image on upload
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.prod_image.path)
        print('\n\nActual Image size conversion--->>> ', img.size)

        # Resize the image as needed
        output_size = (600, 600)  # Set your desired size
        img = img.resize(output_size)
        print('Image size : --->>>',img.size)
        img.save(self.prod_image.path)


class ProductImages(models.Model):
    images = models.ImageField(upload_to='Product-Images')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta: 
        verbose_name_plural = 'Product Images'
        
        # Resizing the image on upload
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.images.path)

        # Resize the image as needed
        output_size = (600, 600)  # Set your desired size
        img.thumbnail(output_size)
        img.save(self.images.path)

class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    color = models.CharField(unique=True,max_length=10, default='Red', blank=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        verbose_name_plural = 'Product Colors'

#############################################  Cart, Orders, OrderItems, Address ########################################################
#############################################  Cart, Orders, OrderItems, Address ########################################################
#############################################  Cart, Orders, OrderItems, Address ########################################################


class CartOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=100, decimal_places=3, default=0.00)
    payment_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=10, blank=True)
    product_status = models.CharField(
        choices=CHOICES, max_length=30, default='Process')

    class Meta:
        verbose_name_plural = 'Cart Orders'
    def __str__(self):
        return f'Order-{self.id}'


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrders, on_delete=models.CASCADE)
    product_id = models.IntegerField(blank=True)
    invoice_no = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=10,blank=True)
    price = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = 'Cart Ordered Items'

################################################# Product review, wishlist, Adderess #####################################
################################################# Product review, wishlist, Adderess #####################################
################################################# Product review, wishlist, Adderess #####################################


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    ratings = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Products Reviews'

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.ratings

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wishlist'

    def __str__(self):
        return self.product.name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    zip_code = models.CharField(max_length=10,blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'
