from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models import Count, Avg
from .models import *
from coreapp.forms import ProductReviewForm
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    categories_with_products = Category.objects.prefetch_related(
        'product_set').filter(product__product_status='publish')
    return render(request, 'coreapp/index.html', context={'categories': categories_with_products})

def store_listing__view(request, cid=None):
    if cid:
        categories_with_products = Category.objects.filter(cid=cid, product__product_status='publish').prefetch_related('product_set').order_by('-created_at')
    else:
        categories_with_products = Category.objects.prefetch_related('product_set').filter(product__product_status='publish').order_by('-created_at')
    
    # categories_with_products = Category.objects.filter(cid=cid, product__product_status='publish').prefetch_related('product_set')

    return render(request, 'coreapp/store.html', context={'categories_with_products': categories_with_products})


def product__view(request, pid):
    product = Product.objects.prefetch_related('productimages_set').get(pid=pid)
    product_reviews = ProductReview.objects.filter(product=product).order_by('-date')
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating = Avg('ratings'))
    product_review_count = ProductReview.objects.filter(product=product).count()
    
    # print(f'\n\nProduct---->>> {product_review_count}')
    
    product_review_form = ProductReviewForm()
    
    # paginator 
    paginator = Paginator(product_reviews, 5)  # Show 10 reviews per page
    page = request.GET.get('page')
    product_review_page = paginator.get_page(page)
    
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user = request.user, product=product).count()
        if user_review_count > 0:
            make_review = False
    print(f'make_review {make_review}')
    
    # print(f'Reviews-->> {product_reviews} ')
    
    related_product = Product.objects.filter(
        category=product.category).exclude(pid=product.pid)
    
    
    # print(f'related Products--->>> {related_product}')
    
    return render(request, 'coreapp/product.html', context={
                                                            'make_review': make_review,
                                                            'product_review_count':product_review_count,
                                                            'products': product, 
                                                            'related_product': related_product, 
                                                            'product_review': product_review_page,
                                                            'average_rating': average_rating,
                                                            'product_review_form':product_review_form,
                                                            })

def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    print(f'\n\nProduct id ---->>>> {product.id}')
    user = request.user
    review = ProductReview.objects.create(
        user= user,
        product = product,
        review = request.POST['review'],
        ratings = request.POST['ratings'],
    )
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating = Avg('ratings'))
    context = {
            'user': user.username,
            'review': request.POST['review'],
            'rating': request.POST['ratings'],
        }
    
    
    return JsonResponse(
        {
        'bool': True,
        'context' : context,
        'average_rating': average_rating,
        }
    )




def search_item(request):
    query = request.GET.get('q')
    products_with_apple = Product.objects.filter(title__icontains=query)
    
    categories_with_products = products_with_apple.select_related('category').prefetch_related('productimages_set', 'productreview_set').order_by('-created_at')
    product_count = Category.objects.annotate(product_count=Count('product'))
    paginator = Paginator(categories_with_products, 20)  # Show 20 products per page
    page = request.GET.get('page')
    product_review_page = paginator.get_page(page)
    
    
    print(f'Searched items: {categories_with_products}')
    for product in categories_with_products:
        print(f'Product: {product}')
        print(f'ImageUrl: {product.prod_image.url}')
        print(f'category: {product.category.name}')
    
    return render(request, 'coreapp/search_product.html', context={'categories_with_products': product_review_page,'product_count': product_count})
    