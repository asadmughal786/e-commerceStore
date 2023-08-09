from django.contrib import admin
from coreapp.models import Product, Category

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','created_at','updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','stock','warrenty','description','created_at','updated_at','category_id']
