from products.models import Category


def categories(request):
    return {'categories_obj': Category.objects.all()}
