from django.contrib import admin
from coreapp.models import *
from django.contrib.auth.models import Group

# Register your models here.

admin.site.unregister(Group)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','created_at','updated_at']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display=['id','sub_name','category']
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','stock','warrenty','description','created_at','updated_at','category']
    list_icon = 'fa fa-product-hunt'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','order_number','product_id','quantity']
    