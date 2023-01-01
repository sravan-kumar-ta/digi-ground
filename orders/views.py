import razorpay
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt

from account.models import Address
from core_folder import settings
from products.models import Cart

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_KEY))


def checkout(request):
    address_id = request.GET['address']
    address = get_object_or_404(Address, id=address_id)
    cart_objs = Cart.objects.filter(user=request.user)

    sub_total = 0
    for i in cart_objs:
        sub_total += i.item_total()

    tax = sub_total * 3 / 100  # 3% tax
    shipping_charge = 40
    discount = sub_total * 2 / 100  # 2% discount
    grand_total = sub_total + tax + shipping_charge - discount

    razorpay_order = razorpay_client.order.create(dict(amount=int(grand_total * 100), currency="INR"))

    context = {
        'address': address,
        'cart_objs': cart_objs,
        'sub_total': sub_total,
        'tax': tax,
        'shipping_charge': shipping_charge,
        'discount': discount,
        'grand_total': grand_total,
        'razorpay_id': settings.RAZORPAY_ID,
        'order_id': razorpay_order['id'],
        'currency': razorpay_order['currency'],
    }
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='login')
@csrf_exempt
def handle_request(request):
    if request.method == "POST":
        try:
            response = request.POST
            params_dict = {
                'razorpay_order_id': response['razorpay_order_id'],
                'razorpay_payment_id': response['razorpay_payment_id'],
                'razorpay_signature': response['razorpay_signature'],
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            return render(request, 'orders/payment_status.html', {'status': True})

        except:
            return render(request, 'orders/payment_status.html', {'status': False})
    else:
        return redirect('products:cart')

