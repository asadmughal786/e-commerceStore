from django.urls import path, include
from coreapp import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'coreapp'


StoreUrlPatterns=[
    # get product
    path("<cid>/", views.store_listing__view, name="category-products"),
    
]

ProductUrlPatterns = [
    path('<pid>/', views.product__view, name='product-detials')
]

SearchUrlPatterns = [
    path('',views.search_item,name='search'),
]
urlpatterns = [
    path('', views.index, name='index'),
    path('product/', include(ProductUrlPatterns)),
    path("store/", include(StoreUrlPatterns)),
    path('search/',include(SearchUrlPatterns)),
    path('ajax-add-review/<int:pid>/',views.ajax_add_review, name='ajax-add-review'),
    path('user/', include('authusers.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
