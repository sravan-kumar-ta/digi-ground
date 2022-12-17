from django.shortcuts import render

from products.models import Category


def home(request):
    categories = Category.objects.all().order_by('?')[:3]  # fetching 3 random objects
    context = {
        'categories': categories,
    }
    return render(request, 'products/home.html', context)
