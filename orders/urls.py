from django.urls import path

from orders import views

urlpatterns = [
    path('proceed-to-checkout', views.checkout, name='checkout'),
]
