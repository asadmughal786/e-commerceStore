from django.db import models
from authusers.models import User
from shortuuid.django_fields import ShortUUIDField
# from django.utils.safestring import mark_safe
import os


# Create your models here.


STATUS_CHOICES = (
    ('process', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)

STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('publish', 'Published'),
)

RATING = (
    ('1', '★☆☆☆☆'),
    ('2', '★★☆☆☆'),
    ('3', '★★★☆☆'),
    ('4', '★★★★☆'),
    ('5', '★★★★★'),
)


def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'


class BaseModel(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


# class tags(models.Model):
#     pass


class Category(BaseModel):
    cid = ShortUUIDField(unique=True, length=10, max_length=30,
                         prefix='cat', alphabet='abcdef12345')
    image = models.ImageField(upload_to='Category', null=True)
    cat = models.Manager()

    class Meta:
        verbose_name_plural = 'Categories'

    # def catgory_image(self):
    #     # Corrected
    #     return mark_safe('<img src="/media/%s" width= "50px" height = "50px">' % (self.image.url))

    def __str__(self):
        return self.name

# class SubCategory(models.Model):
#     subcatid = ShortUUIDField(
#         unique=True, length=10, max_length=30, prefix='scat', alphabet='abcdef12345')
#     sub_title = models.CharField(max_length=50)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

#     class Meta:
#         verbose_name_plural = 'Sub Categories'

#     def __str__(self):
#         return self.sub_title


class Product(BaseModel):
    def product_image_path(instance, filename):
        # Corrected
        return os.path.join(instance.category.name, instance.name, filename)

    prod_image = models.ImageField(
        upload_to=product_image_path, blank=True, null=True, default='static/img/logo.png')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None)

    pid = ShortUUIDField(unique=True, length=10, max_length=30,
                         prefix='scat', alphabet='abcdef12345')
    title = models.CharField(max_length=100, default='New Product')
    specification = models.TextField(
        null=True, blank=True, default='No description')
    description = models.TextField(max_length=500, blank=True)

    qty = models.PositiveIntegerField(default=0)
    warrenty = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00)
    old_price = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00)

    # prod_tags = models.ForeignKey(tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(
        choices=STATUS, max_length=10, default='in_review')

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)

    sku = ShortUUIDField(unique=True, length=4, max_length=20,
                         prefix='sku', alphabet='1234567890')

    prod = models.Manager()

    class Meta:
        verbose_name_plural = 'Products'

    # def product_image(self):
    #     return mark_safe('<img src="/media/%s" width= "50px" height = "50px">' % (self.prod_image.url))

    def __str__(self):
        return self.name

    def get_percentage(self):
        new_price = (self.price/self.old_price) * 100
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(upload_to='Product-Images')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'


#############################################  Cart, Orders, OrderItems, Address ########################################################
#############################################  Cart, Orders, OrderItems, Address ########################################################
#############################################  Cart, Orders, OrderItems, Address ########################################################


class CartOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=100, decimal_places=3, default=0.00)
    payment_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(
        choices=STATUS_CHOICES, max_length=30, default='process')

    class Meta:
        verbose_name_plural = 'Cart Orders'


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrders, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    invoice_no = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = 'Cart Ordered Items'

    def CartorderItems_img(self):
        return mark_safe('<img src="/media/%s" width= "50px" height = "50px">' % (self.image))


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
        return self.product.name

    def get_rating(self):
        return self.ratings


class ProductImages(models.Model):
    images = models.ImageField(
        upload_to='product-image', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Product Image'


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
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'
