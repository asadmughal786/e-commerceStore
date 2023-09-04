from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    # return HttpResponse("THis is new page")
    return render(request,'coreapp/index.html')

def product_view(request):
    return render(request,'coreapp/product-view.html')