from django.shortcuts import get_object_or_404, render, redirect

from account.models import Address
from products.models import Cart


def checkout(request):
    try:
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

        context = {
            'address': address,
            'cart_objs': cart_objs,
            'sub_total': sub_total,
            'tax': tax,
            'shipping_charge': shipping_charge,
            'discount': discount,
            'grand_total': grand_total,
        }
        return render(request, 'products/checkout.html', context)
    except:
        return redirect('products:cart')
