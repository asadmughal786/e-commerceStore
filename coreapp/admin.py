from django.contrib import admin
from coreapp.models import *
from django.contrib.auth.models import Group
from django.utils.html import format_html

# Register your models here.

admin.site.unregister(Group)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'avatar_tag', 'created_at', 'updated_at']

    def avatar_tag(self, obj):
        if obj.image:
            return format_html( f'<img src="{obj.image.url}"  align = "middle" width="60px" height="60px"/>')
        else:
            return "No Image"
    avatar_tag.short_description = 'Avatar'

# ------------------------------------- Products ----------------------------------------------

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductColorAdmin(admin.TabularInline):
    model = ProductColor

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    inlines = [ProductImagesAdmin, ProductColorAdmin]
    list_display = ['title', 'avatar_tag',
                    'in_stock', 'qty', 'warrenty', 'price', 'category', 'product_status']
    fieldsets =(
        ("General Information",{'fields':('pid','sku','avatar_tag','prod_image','title','category','specification','description','qty','price','old_price','warrenty','in_stock','product_status')}),
    )
    readonly_fields = ['pid','sku','avatar_tag']
    
    def avatar_tag(self, obj):
        if obj.prod_image:
            return format_html( f'<img src="{obj.prod_image.url}"  align = "middle" width="60px" height="60px"/>')
        else:
            
            return 'No image'
    avatar_tag.short_description = 'Avatar'
    avatar_tag.allow_tags = True
    
@admin.register(CartOrders)
class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['payment_status','product_status']
    list_display = ['id','user', 'price', 'payment_status','payment_type',
                    'order_date', 'product_status']


@admin.register(CartOrderItems)
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['invoice_no', 'item','product_id','color',
                    'avatar_tag', 'qty', 'price', 'total_amount']
    def avatar_tag(self, obj):
        if isinstance(obj.image, str):
            return format_html(f'<img src="{obj.image}" align="middle" width="60px" height="60px"/>')
        elif obj.image:
            return format_html(f'<img src="{obj.image.url}" align="middle" width="60px" height="60px"/>')
        else:
            return 'No image'
    avatar_tag.short_description = 'Avatar'
    avatar_tag.allow_tags = True


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
