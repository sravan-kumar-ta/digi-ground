from django.urls import path
from django.views.generic import TemplateView

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('categories', TemplateView.as_view(template_name='products/categories.html'), name='category'),
    path('<slug:category_slug>/', views.product_list, name='products-list'),
    path('<slug:c_slug>/<slug:p_slug>', views.details_of_medicine, name='category'),
]
