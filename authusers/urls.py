from django.urls import path,include
from . import views


app_name = 'authusers'

urlpatterns = [
    path('sign-up/',views.register_view,name='sign-up'),
    path('sign-in/',views.login_view,name='sign-in'),
    path('log-out/',views.logout_view,name='logout'),
    path('changepass/',views.changepass1,name='user_change_pass'),
    path('user-profile/',views.user_profile, name='user-profile'),
]