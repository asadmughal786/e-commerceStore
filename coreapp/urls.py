from django.urls import path, include
from coreapp import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'coreapp'


StoreUrlPatterns=[
    # get product
    path("",views.store_listing__view, name='store-view'),
    path("<cid>/", views.store_listing__view, name="category-products"),
    
]

ProductUrlPatterns = [
    path('<pid>/', views.product__view, name='product-detials')
]

SearchUrlPatterns = [
    path('',views.search_item,name='search'),
]

AddToCartUrlPatterns = [
    
    path('',views.added_to_cart, name='add-to-cart'),
    
]

urlpatterns = [
    path('', views.index, name='index'),
    path('product/', include(ProductUrlPatterns)),
    path("store/", include(StoreUrlPatterns)),
    path('search/',include(SearchUrlPatterns)),
    path('add-to-cart/',include(AddToCartUrlPatterns)),
    path('cart/', views.cart_view, name='cart'),
    path('ajax-add-review/<int:pid>/',views.ajax_add_review, name='ajax-add-review'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
