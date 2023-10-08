from django.urls import path, include
from coreapp import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'coreapp'


StoreUrlPatterns=[
    # get product
    path("", views.store_listing__view, name="category-products"),
    
]


urlpatterns = [
    path('', views.index, name='index'),
    path('product/<pid>/', views.product__view, name='product-detials'),
    path('ajax-add-review/<int:pid>/',views.ajax_add_review, name='ajax-add-review'),
    path('user/', include('authusers.urls')),
    path("store/", include(StoreUrlPatterns)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
