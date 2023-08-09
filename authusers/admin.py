from django.contrib import admin
from authusers.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','user_phone','is_staff']

admin.site.register(User, UserAdmin)