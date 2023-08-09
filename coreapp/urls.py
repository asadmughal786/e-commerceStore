from django.urls import path, include
from coreapp import views


app_name = 'coreapp'

urlpatterns = [
    path('',views.index,name='index'),
    path('user/',include('authusers.urls')),
]