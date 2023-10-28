from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SignUpForm(UserCreationForm):
    user_phone = forms.CharField(label='Phone number',required=True,help_text='Enter Phone number in this formate "03XXXXXXXXX"',validators=[RegexValidator(regex=r'^(\+92|0)?(3\d{9})$',
        message='Enter a valid Pakistan phone number.')])
   
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email','user_phone']
        # labels = {'username': 'Username', 'first_name': 'First Name', 'last_name': 'Last Name', 'email':'Email Address'}



class CustomAuthenticationForm(AuthenticationForm):
        # Disable autocomplete for form fields
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-class', 'autocomplete':'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-class','autocomplete':'off'}))


class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields =['username','first_name','last_name','email','date_joined','last_login']
        labels = {'email':'Email'}


# class EditAdminProfileForm(UserChangeForm):
#     password = None
#     class Meta:
#         model = Users
#         fields ='__all__'
#         labels = {'email':'Email'}