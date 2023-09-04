from django.contrib import admin
from coreapp.models import *
from django.contrib.auth.models import Group
from django.utils.html import format_html

# Register your models here.

admin.site.unregister(Group)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'avatar_tag', 'created_at', 'updated_at']

    def avatar_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}"  align = "middle" width="60px" height="60px"/>'.format(obj.image.url))
        else:
            return "No Image"
    avatar_tag.short_description = 'Avatar'

# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display=['id','sub_title','category']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'avatar_tag',
                    'in_stock', 'qty', 'warrenty', 'description', 'category']

    def avatar_tag(self, obj):
        if obj.prod_image:
            return format_html('<img src="{}" align = "middle" width="100px" height="100px"/>'.format(obj.prod_image.url))
        else:
            return "No Image"
    avatar_tag.short_description = 'Avatar'


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['product', 'images']


@admin.register(CartOrders)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'payment_status',
                    'order_date', 'product_status']


@admin.register(CartOrderItems)
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item',
                    'image', 'qty', 'price', 'total_amount']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'ratings', 'date']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id','order_number','product_id','quantity']
