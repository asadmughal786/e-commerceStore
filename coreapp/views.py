from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Count, Avg
from .models import *
from coreapp.forms import ProductReviewForm
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    categories = Category.objects.all()
    published_products = Product.objects.filter(product_status='publish').select_related('category')
    published_products = published_products.prefetch_related('productimages_set', 'productcolor_set')
    # Annotate the average rating for each product
    published_products = published_products.annotate(average_rating=Avg('productreview__ratings'))
    # Annotate the count of images for each product
    published_products = published_products.annotate(image_count=Count('productimages'))
    
    for product in published_products:
        print("ID:", product.id)
        print("Pid:", product.pid)
        print("Title:", product.title)
        print("Category:", product.category.name)
        print("Average Rating:", product.average_rating)
        print("Image Count:", product.image_count)
        print("Colors:")
        for color in product.productcolor_set.all():
            print(color.color)
            
            
    return render(request, 'coreapp/main-index.html', context={
        'categories': categories,
        'categories_products': published_products})



def store_listing__view(request, cid=None):
    categories = Category.objects.all()
    if cid:
        print('Cid part is running')
        categories_with_products = Product.objects.filter(category__cid=cid, product_status='publish').prefetch_related("productcolor_set").annotate(average_review=Avg('productreview__ratings')).order_by('-created_at')

    else:
        print('Entered in Else part')
        categories_with_products = Product.objects.filter(product__product_status='publish').prefetch_related('product_set').annotate(average_rating=Avg('productreview__ratings')).order_by('-created_at')
    
    for product in categories_with_products:
        print(f"Product Name: {product.title}")
        print(f"Category Name: {product.category.name}")

        # Check if there are reviews and calculate the average
        if product.average_review is not None:
            print(f"Average Review: {product.average_review:.2f}")
        else:
            print("No reviews available")

        # Check for product colors
        colors = product.productcolor_set.all()
        if colors:
            print("Available Colors:")
            for color in colors:
                print(f"- {color.color}")
        else:
            print("No colors available")

        # Include other product details as needed
        print(f"Price: {product.price}")
    
    
    
    
    # Paginator
    category_with_products_per_page = _extracted_from_store_listing__view_20(
        categories_with_products, request
    )   
    

    return render(request, 'coreapp/product-listing.html', context={
        'all_categories': categories,
        'categories_with_products': category_with_products_per_page})

# Paginator Funtion

# TODO Rename this here and in `store_listing__view`
def _extracted_from_store_listing__view_20(categories_with_products, request):
    paginator = Paginator(categories_with_products, 20)  # Show 20 products per page
    page = request.GET.get('page')
    return paginator.get_page(page)


def product__view(request, pid):
    product = Product.objects.prefetch_related('productimages_set','productcolor_set').get(pid=pid)
    print('Product Data--->>> ', product.id)
    for product_color in product.productcolor_set.all():
        print("Color:", product_color.color)
        
    product_reviews = ProductReview.objects.filter(product=product).order_by('-date')
    print('product reviews---->>',product_reviews)
    average_product_rating = ProductReview.objects.filter(product=product ).aggregate(rating = Avg('ratings'))
    print("Average Rating From Product View",average_product_rating)
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
                                                            'average_prod_rating': average_product_rating,
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
    # print('Average rating from Ajax',average_rating)
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
    
    #paginator
    paginator = Paginator(categories_with_products, 20)  # Show 20 products per page
    page = request.GET.get('page')
    product_review_page = paginator.get_page(page)
    
    
    return render(request, 'coreapp/search_product.html', context={'categories_with_products': product_review_page,'product_count': product_count})

# Add to cart ajax

def added_to_cart(request):
    cart_products = {
        str(request.GET["id"]): {
            'title': request.GET["title"],
            'qty': request.GET['qty'],
            'price': request.GET['price'],
            'color': request.GET['color'],
            'image': request.GET['image'],
            'pid': request.GET['pid'],
        }
    }
    
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        if str(request.GET['id']) in cart_data:
            cart_data[str(request.GET['id'])]['qty'] = int(request.GET['qty'])
        else:
            cart_data.update(cart_products)
        request.session['cart_data_obj'] = cart_data
    else:
        # Initialize cart_data_obj as an empty dictionary
        request.session['cart_data_obj'] = cart_products

    return JsonResponse({
        "data": request.session["cart_data_obj"],
        'totalCartItems': len(request.session['cart_data_obj'])
    })

# Cart View

def cart_view(request):
    cart_total_amount = 0
    
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            return render(request, "coreapp/checkout.html",{
                "cart_data": request.session["cart_data_obj"],
                'totalCartItems': len(request.session['cart_data_obj']),
                "TotalAmount": cart_total_amount
                                                            
                })
        else:
            messages.warning(request,"You cart is empty")
            return redirect("coreapp:index")