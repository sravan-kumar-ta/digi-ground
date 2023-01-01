from django.urls import path

from orders import views

urlpatterns = [
    path('proceed-to-checkout', views.checkout, name='checkout'),
    path('handle-request', views.handle_request, name='handle_request'),
]
