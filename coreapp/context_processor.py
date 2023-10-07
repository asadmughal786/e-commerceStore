from .models import Category


def default(request):
    categories = Category.cat.all()
    return{'categories':categories}