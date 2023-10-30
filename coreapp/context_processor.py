from .models import Category, Address, Product
from django.db.models import Min,Max


def default(request):
    categories = Category.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    print(f'Print the categories from the context {min_max_price}')
    try:
        address = Address.objects.get(user = request.user)
        
    except Exception:
        address = None
    return{
        'categories':categories,
        'address': address,
        'min_max_price': min_max_price,

        }