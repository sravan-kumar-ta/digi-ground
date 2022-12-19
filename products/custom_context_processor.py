from django.db.models import Min, Max

from products.models import Category, Product


def categories(request):
    return {'categories_obj': Category.objects.all()}


def get_filters(request):
    minMaxPrice = Product.objects.aggregate(Min('price'), Max('price'))
    data = {
        'minMaxPrice': minMaxPrice,
    }
    return data
