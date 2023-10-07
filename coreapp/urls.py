from django.urls import path, include
from coreapp import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'coreapp'

urlpatterns = [
    path('', views.index, name='index'),
    path("store/", views.store_listing__view, name="category-products"),
    path('product/<pid>/', views.product__view, name='product-detials'),
    path('user/', include('authusers.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
