import time

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView
from products.models import Category, Product, Brand


class HomeView(TemplateView):
    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = {
            'categories': Category.objects.all().order_by('?')[:3],  # fetching 3 random objects
            'products': Product.objects.all().order_by('?')[:8]  # fetching 3 random objects
        }
        return context


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/category_products.html'
    category = None

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return super().get_queryset().filter(Q(category=self.category) & Q(stock__gte=1))  # stock >= 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['category'] = self.category
        context['brands'] = Brand.objects.filter(category=self.category)
        return context


def product_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(Q(category=category) & Q(stock__gte=1))
    brands = Brand.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
        'brands': brands
    }
    return render(request, 'products/category_products.html', context)


def products_filter(request):
    time.sleep(2)
    category = request.GET.getlist('category')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    selected_brands = request.GET.getlist('brands[]')
    price_range = request.GET['price_range']

    category_obj = get_object_or_404(Category, title=category[0])
    all_products = Product.objects.filter(Q(category=category_obj) & Q(stock__gte=1))
    all_products = all_products.filter(Q(price__gte=minPrice) & Q(price__lte=maxPrice))
    if len(selected_brands) is not 0:
        selected_brands_objs = list()
        for brand in selected_brands:
            selected_brands_objs.append(get_object_or_404(Brand, name=brand))
        all_products = all_products.filter(brand__in=selected_brands_objs)

    if price_range:
        if price_range is '1':
            all_products = all_products.order_by('price')
        elif price_range is '2':
            all_products = all_products.order_by('-price')

    template = render_to_string('ajax/products.html', {'products': all_products})
    return JsonResponse({'data': template})


def details_of_medicine(request, c_slug, p_slug):
    product = get_object_or_404(Product, slug=p_slug)
    related_products = Product.objects.exclude(id=product.id).filter(category__slug=c_slug)

    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'products/detail.html', context)
