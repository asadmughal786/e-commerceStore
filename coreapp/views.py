from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.


def index(request):
    categories_with_products = Category.cat.prefetch_related(
        'product_set').filter(product__product_status='publish')
    return render(request, 'coreapp/index.html', context={'categories': categories_with_products})

def store_listing__view(request):
    categories_with_products = Category.cat.prefetch_related(
        'product_set').filter(product__product_status='publish')
    return render(request, 'coreapp/store.html', context={'categories_with_products': categories_with_products})


def product__view(request, pid):
    product = Product.prod.prefetch_related('productimages_set').get(pid=pid)
    related_product = Product.prod.filter(
        category=product.category).exclude(pid=product.pid)
    print(f'related Products--->>> {related_product}')
    return render(request, 'coreapp/product.html', context={'products': product, 'related_product': related_product})
