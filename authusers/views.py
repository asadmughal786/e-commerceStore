from django.shortcuts import render,redirect,HttpResponseRedirect
from authusers.models import User
from .forms import SignUpForm, CustomAuthenticationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
# Create your views here.

def register_view(request):
    if request.method == 'POST':
        print("----------------> getting the request", dict(request.POST.items()))
        request_data = dict(request.POST.items())
        form = SignUpForm(request.POST or None)

        print('Boolean------>',request_data is form.data)
        print('Form Data: ', form.data)
        if form.is_valid():

            form.save()
            print('-----------> User regitsered')
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hey {username}, Your Account created Successfully!')

            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            login(request,new_user)
            return redirect('/')
        else:
            print(form.errors)
    else:
        form = SignUpForm()

    context = {
        'form':form
    }
    return render(request,'authusers/signup.html',context)

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



def logout_view(request):
    logout(request)
    messages.success(request, "Logout successfully!")
    return redirect('/')

        