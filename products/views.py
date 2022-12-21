import time

from django.core.paginator import Paginator
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


def product_filter(*args, **kwargs):
    selected_brands = kwargs['data']['selected_brands']
    sort_method = kwargs['data']['sort_method']
    min_price = kwargs['data']['min_price']
    max_price = kwargs['data']['max_price']
    products = args[0]

    if len(selected_brands) != 0:
        selected_brands_objs = list()
        for brand in selected_brands:
            selected_brands_objs.append(get_object_or_404(Brand, name=brand))
        products = products.filter(brand__in=selected_brands_objs)

    if sort_method:
        if sort_method == '1':
            products = products.order_by('price')
        elif sort_method == '2':
            products = products.order_by('-price')

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return products


def product_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(Q(category=category) & Q(stock__gte=1))
    brands = Brand.objects.filter(category=category)
    category_id = category.id

    context = dict()

    # filtering the products
    if request.method == 'POST':
        selected_brands = request.POST.getlist('brands')
        sort_method = request.POST['sort']
        min_price = request.POST['min']
        max_price = request.POST['max']

        session_filter = {
            'cat_id': category_id,
            'selected_brands': selected_brands,
            'sort_method': sort_method,
            'min_price': min_price,
            'max_price': max_price
        }
        context.update(session_filter)

        # filtering the products
        products = product_filter(products, data=session_filter)

        request.session['session_filter'] = session_filter

    # this block is used to filter the data when pagination is occurs...(when changing pages)
    if request.method == 'GET':
        if 'session_filter' in request.session:
            if request.session['session_filter']['cat_id'] == category_id:
                session_filter = request.session['session_filter']
                context.update(session_filter)
                # filtering the products
                products = product_filter(products, data=session_filter)
            else:
                request.session.flush()
        try:
            if request.GET['clear_filter'] == '1':
                # clearing filter and reset to default products fetching
                request.session.flush()
                context.pop('cat_id')
                context.pop('selected_brands')
                context.pop('sort_method')
                context.pop('min_price')
                context.pop('max_price')
                products = Product.objects.filter(Q(category=category) & Q(stock__gte=1))
        except:
            pass

    # Pagination
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context.update({
        'category': category,
        'page_obj': page_obj,
        'brands': brands
    })
    return render(request, 'products/category_products.html', context)


def details_of_medicine(request, c_slug, p_slug):
    product = get_object_or_404(Product, slug=p_slug)
    related_products = Product.objects.exclude(id=product.id).filter(category__slug=c_slug)

    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'products/detail.html', context)
