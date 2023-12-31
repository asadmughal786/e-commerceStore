from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Subquery
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template.loader import render_to_string
from django.db.models import Count, Avg
from .models import Product, ProductReview, Category
from coreapp.forms import ProductReviewForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    categories = Category.objects.all()
    published_products = Product.objects.filter(
        product_status='publish').select_related('category')
    published_products = published_products.prefetch_related(
        'productimages_set', 'productcolor_set')
    # Annotate the average rating for each product
    published_products = published_products.annotate(
        average_rating=Avg('productreview__ratings'))
    # Annotate the count of images for each product
    published_products = published_products.annotate(
        image_count=Count('productimages'))

    products_with_high_ratings = Product.objects.annotate(
        average_rating=Avg('productreview__ratings')
    ).filter(productreview__ratings__gt=4)

    # Print the products
    # if products_with_high_ratings:
    #     for product in products_with_high_ratings:
    #         print(f'Product ID: {product.id}')
    #         print(f"Product Title: {product.title}")
    #         print(f"Product Description: {product.description}")
    #         print(f'Product Image: "{product.prod_image.url}')
    #         print(f"Product Price: {product.price}")
    #         print(f"Product Category: {product.category.name}")
    #         print(f"Average Rating: {product.average_rating:.2f}")
    #         print("\n")
    # else:
    #     print('No products yet')

    # for product in published_products:
    #     print("ID:", product.id)
    #     print("Pid:", product.pid)
    #     print("Title:", product.title)
    #     print("Category:", product.category.name)
    #     print("Average Rating:", product.average_rating)
    #     print("Image Count:", product.image_count)
    #     print("Colors:")
    #     for color in product.productcolor_set.all():
    #         print(color.color)

    return render(request, 'coreapp/main-index.html', context={
        'categories': categories,
        'categories_products': published_products,
        'top_products': products_with_high_ratings,
        })


def store_listing__view(request, cid=None):
    categories = Category.objects.all()
    products_with_high_ratings = Product.objects.annotate(
        average_rating=Avg('productreview__ratings')
        ).filter(productreview__ratings__gt=4)
    print(products_with_high_ratings)
    if cid:
        print('Cid part is running')
        categories_with_products = Product.objects.filter(category__cid=cid, product_status='publish').prefetch_related(
            "productcolor_set").annotate(average_review=Avg('productreview__ratings')).order_by('-created_at')

    else:
        print('Entered in Else part')
        categories_with_products = Product.objects.filter(product__product_status='publish').prefetch_related(
            'product_set').annotate(average_rating=Avg('productreview__ratings')).order_by('-created_at')
        
        

    # for product in categories_with_products:
    #     print(f"Product Name: {product.title}")
    #     print(f"Category Name: {product.category.name}")

    #     # Check if there are reviews and calculate the average
    #     if product.average_review is not None:
    #         print(f"Average Review: {product.average_review:.2f}")
    #     else:
    #         print("No reviews available")

    #     # Check for product colors
    #     colors = product.productcolor_set.all()
    #     if colors:
    #         print("Available Colors:")
    #         for color in colors:
    #             print(f"- {color.color}")
    #     else:
    #         print("No colors available")

    #     # Include other product details as needed
    #     print(f"Price: {product.price}")

    # Paginator
    category_with_products_per_page = _extracted_from_store_listing__view_20(
        categories_with_products, request
    )

    return render(request, 'coreapp/product-listing.html', context={
        'all_categories': categories,
        'top_products': products_with_high_ratings,
        'categories_with_products': category_with_products_per_page})

# Paginator Funtion

# TODO Rename this here and in `store_listing__view`


def _extracted_from_store_listing__view_20(categories_with_products, request):
    # Show 20 products per page
    paginator = Paginator(categories_with_products, 20)
    page = request.GET.get('page')
    return paginator.get_page(page)


def product__view(request, pid):
    product = Product.objects.prefetch_related(
        'productimages_set', 'productcolor_set').get(pid=pid)
    print('Product Data--->>> ', product.id)
    for product_color in product.productcolor_set.all():
        print("Color:", product_color.color)

    product_reviews = ProductReview.objects.filter(
        product=product).order_by('-date')
    print('product reviews---->>', product_reviews)
    average_product_rating = ProductReview.objects.filter(
        product=product).aggregate(rating=Avg('ratings'))
    print("Average Rating From Product View", average_product_rating)
    product_review_count = ProductReview.objects.filter(
        product=product).count()

    # print(f'\n\nProduct---->>> {product_review_count}')

    product_review_form = ProductReviewForm()

    # paginator
    paginator = Paginator(product_reviews, 5)  # Show 10 reviews per page
    page = request.GET.get('page')
    product_review_page = paginator.get_page(page)

    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(
            user=request.user, product=product).count()
        if user_review_count > 0:
            make_review = False
    print(f'make_review {make_review}')

    # print(f'Reviews-->> {product_reviews} ')

    related_product = Product.objects.filter(
        category=product.category).exclude(pid=product.pid)

    # print(f'related Products--->>> {related_product}')

    return render(request, 'coreapp/product.html', context={
        'make_review': make_review,
        'product_review_count': product_review_count,
        'products': product,
        'related_product': related_product,
        'product_review': product_review_page,
        'average_prod_rating': average_product_rating,
        'product_review_form': product_review_form,
    })


def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    print(f'\n\nProduct id ---->>>> {product.id}')
    user = request.user
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        ratings=request.POST['ratings'],
    )
    average_rating = ProductReview.objects.filter(
        product=product).aggregate(rating=Avg('ratings'))
    # print('Average rating from Ajax',average_rating)
    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['ratings'],
    }

    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_rating': average_rating,
        }
    )


def search_item(request):
    query = request.GET.get('q')
    categories_with_products = Product.objects.filter(title__icontains=query, product_status='publish').prefetch_related(
        "productcolor_set").annotate(average_review=Avg('productreview__ratings')).order_by('-created_at')
    product_count = Category.objects.annotate(product_count=Count('product'))

    # paginator
    # Show 20 products per page
    paginator = Paginator(categories_with_products, 20)
    page = request.GET.get('page')
    product_review_page = paginator.get_page(page)

    return render(request, 'coreapp/search_product.html', context={'categories_with_products': product_review_page, 'product_count': product_count})


# Add to cart ajax

def added_to_cart(request):
    cart_products = {
        str(request.GET["id"]): {
            'id': request.GET["id"],
            'title': request.GET["title"],
            'qty': int(request.GET['qty']),  # Ensure quantity is an integer
            'price': request.GET['price'],
            'color': request.GET['color'],
            'image': request.GET['image'],
            'pid': request.GET['pid'],
        }
    }

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        product_id = str(request.GET['id'])

        if product_id in cart_data:
            # Product already exists in the cart, update the quantity
            cart_data[product_id]['qty'] += int(request.GET['qty'])
        else:
            # Product doesn't exist in the cart, add it
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
    print(request.session)
    if 'cart_data_obj' in request.session and (len(request.session['cart_data_obj']) > 0):
        print("Entered in View Cart")
        cart_total_amount = 0
        total_amount = 0
        # cart total amount
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            print('\nTotal Cart Amount--->>', cart_total_amount)

        return render(request, "coreapp/checkout.html", {"cart_data": request.session["cart_data_obj"], 'totalCartItems': len(request.session['cart_data_obj']),
                                                         "TotalAmount": cart_total_amount
                                                         })

    else:
        print("else part is working")
        messages.warning(request, "Your cart is empty")
        return redirect("coreapp:index")


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session and product_id in request.session['cart_data_obj']:
        cart_data = request.session["cart_data_obj"]
        del request.session['cart_data_obj'][product_id]
        request.session['cart_data_obj'] = cart_data
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    context = render_to_string("coreapp/async/cart-checkout.html", {"cart_data": request.session["cart_data_obj"], 'totalCartItems': len(request.session['cart_data_obj']),
                                                                    "TotalAmount": cart_total_amount
                                                                    })
    return JsonResponse({
        "data": context,
        'totalCartItems': len(request.session['cart_data_obj'])
    })


def checkout_view(request):
    if request.user.is_authenticated:
        if 'cart_data_obj' in request.session:
            return _extracted_from_checkout_view_4(request)
    else:
        messages.error(
            request, "Please login First to proceed with your order")
        return redirect("authusers:sign-in")


# TODO Rename this here and in `checkout_view`
def _extracted_from_checkout_view_4(request):
    cart_total_amount = 0
    total_amount = 0
    # cart total amount
    for product_id, item in request.session['cart_data_obj'].items():
        total_amount += int(item['qty']) * float(item['price'])
        print('\nTotal Cart Amount--->>', total_amount)

    # Cart Order Object Creating
    order = CartOrders.objects.create(
        user=request.user,
        payment_type='COD',
        price=total_amount,
    )
    for product_id, item in request.session['cart_data_obj'].items():
        cart_total_amount += int(item['qty']) * float(item['price'])
        # print('\nTotal Cart Amount--->>', cart_total_amount)
        cart_order_products = CartOrderItems.objects.create(
            order=order,
            invoice_no=f"INVOICE-NO-{order.id}",
            product_id=item['id'],
            item=item['title'],
            image=item['image'],
            qty=item['qty'],
            color=item['color'],
            price=item['price'],
            total_amount=float(item['qty']) * float(item['price'])
        )
    if 'cart_data_obj' in request.session:
        del request.session['cart_data_obj']
    messages.success(request, 'Thank you! Your order has been placed')
    return redirect("coreapp:index")


def invoice_view(request):
    return render(request, 'coreapp/invoice.html')
