from django.shortcuts import render,redirect,HttpResponseRedirect
from authusers.models import User
from .forms import SignUpForm, CustomAuthenticationForm, EditUserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import login, authenticate,logout,update_session_auth_hash
from django.contrib import messages
from coreapp.models import CartOrders, CartOrderItems, Address
# Create your views here.

def register_view(request):
    if request.method == 'POST':
        # print("----------------> getting the request", dict(request.POST.items()))
        # request_data = dict(request.POST.items())
        form = SignUpForm(request.POST or None)

        # print('Boolean------>',request_data is form.data)
        # print('Form Data: ', form.data)
        if form.is_valid():
            return _extracted_from_register_view_10(form, request)
    else:
        form = SignUpForm()

    context = {
        'form':form
    }
    return render(request,'authusers/signup.html',context)


# TODO Rename this here and in `register_view`
def _extracted_from_register_view_10(form, request):
    form.save()
    print('-----------> User regitsered')
    username = form.cleaned_data.get('username')
    messages.success(request, f'Hey {username}, Your Account created Successfully!')

    new_user = authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password1'])
    login(request,new_user)
    return redirect('/')

def login_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('/')
    if request.method == "POST":
        form = CustomAuthenticationForm(request=request, data=request.POST)
        # print(form.data)
        # print(form.errors)
        if form.is_valid():
            u_name = form.cleaned_data['username']
            u_pass = form.cleaned_data['password']
            user = authenticate(email=u_name, password=u_pass)
            if user is not None:
                login(request, user)
                messages.success(request, 'User login Succeessfully!')
                return HttpResponseRedirect('/')
        else:
            print('You are not authorized')
            messages.error(request, 'You are not authorized, Please Create the Account to login')
                
    else:
        form = CustomAuthenticationForm()           
    return render(request, 'authusers/login.html',{'form':form})

@login_required
def user_profile(request):
    if request.method == "POST":
        form = EditUserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Updated Successfully!')
            update_session_auth_hash(request, form.user)  # Update the session to avoid logout
    else:
        form = EditUserProfileForm(instance=request.user)
    
    return render(request, 'authusers/profile.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logout successfully!")
    return redirect('/')

def changepass1 (request):
    if request.user.is_authenticated:
        if request.method =="POST":
            form = SetPasswordForm(user= request.user,data=request.POST)
            if form.is_valid():
                form.save()
                #This function is user to maintain the session for the user.
                update_session_auth_hash(request,form.user)
                messages.info(request,'Password Saved Successfully!')
                return redirect('authusers:user_change_pass')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request,'authusers/changepassword.html',{"form": form})
    else:
        messages.error(request,'You have no rights to access this page!')
        return redirect('authusers:sign-up')
    

def orders_views(request):
    if request.user.is_authenticated:
        orders = CartOrders.objects.filter( user=request.user).order_by('-id')
        return render(request,'authusers/orders.html',{'orders':orders})
    else:
        messages.error(request,"Please login First to proceed with your order")
        return redirect('authusers:sign-in')

def order_detail_view(request,id):
    if request.user.is_authenticated:
        order = CartOrders.objects.get(user=request.user,id=id)
        products = CartOrderItems.objects.filter(order=order)
        print(f"order items: {products.values()}")
        return render(request, 'authusers/orderdetails.html', {'products':products})  
    else:
        messages.error(request, "Please Login first to see the Orders Details")
        

def create_address(request):
    if request.user.is_authenticated:
        addresss = Address.objects.filter(user = request.user)
        
        