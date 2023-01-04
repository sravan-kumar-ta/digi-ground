from django.urls import path

from orders import views

urlpatterns = [
    path('proceed-to-checkout', views.checkout, name='checkout'),
    path('handle-request', views.handle_request, name='handle_request'),
    path('my-orders', views.orders, name='orders'),
    path('my-orders/<int:o_id>', views.order_detail, name='order_detail'),
    path('generate-invoice/<int:o_id>/Payment-Invoice', views.generate_invoice, name='generate_invoice'),
]
