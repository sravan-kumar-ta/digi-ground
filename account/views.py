import requests
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView

from account.CustomBackend import CustomAuth
from account.forms import CustomUserCreationForm, LoginForm, ChangePasswordForm, ResetPasswordForm
from account.models import CustomUser, Address
from products.models import Product, Cart, Wishlist


class RegistrationView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "account/register.html"
    success_url = reverse_lazy("login")


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = CustomAuth.authenticate(self.request, username=username, password=password)

        if user:
            if not user.is_active:
                # Here we have to build a phone number validation for activating user account.
                # messages.error(self.request, "You have not activated your account.")
                # return redirect('login')
                user.is_active = True
                user.save()
                if 'cart' in self.request.session:
                    session_cart = self.request.session['cart']
                    for i in session_cart:
                        item = session_cart[i]
                        product = get_object_or_404(Product, id=i)
                        quantity = item['qty']
                        cart_item = Cart.objects.create(product=product, user=user, quantity=quantity)
                        cart_item.save()
            login(request=self.request, user=user)
            self.request.session['cart_length'] = Cart.objects.filter(user=self.request.user).count()
            messages.success(self.request, 'Successfully logged in')

            # If url have next page
            url = self.request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('products:home')

        else:
            messages.error(self.request, "Invalid credentials..!")
            return redirect('login')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Credentials')
        return redirect('login')


def profile(request):
    addresses = Address.objects.filter(user=request.user)

    return render(request, 'account/profile.html', {'addresses': addresses})


class WishlistView(ListView):
    model = Wishlist
    context_object_name = 'wishlist'
    template_name = 'account/wishlist.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


def add_to_wishlist(request):
    p_id = request.GET['prod_id']
    product = get_object_or_404(Product, id=p_id)
    try:
        obj = Wishlist.objects.create(product=product, user=request.user)
        obj.save()
        messages.success(request, 'Item added to your wishlist.')
    except:
        data = 0
    else:
        data = 1

    # The data will be checked in ajax. If 1, redirect to wishlist page.
    return JsonResponse({'data': data})


def remove_from_wishlist(request, p_id):
    product = get_object_or_404(Product, id=p_id)
    obj = Wishlist.objects.get(product=product, user=request.user)
    obj.delete()
    messages.error(request, 'Item remove from your wishlist.')
    return redirect('wishlist')


def add_address(request):
    if request.method == 'POST':
        try:
            pin_code = request.POST['pin']
            state = request.POST['state']
            district = request.POST['district']
            locality = request.POST['locality']
            phone = request.POST['phone']
            address = Address.objects.create(
                pin_code=pin_code,
                state=state,
                district=district,
                locality=locality,
                phone_number=phone,
                user=request.user
            )
            address.save()
            messages.success(request, 'Successfully added your address.')
            return redirect('profile')
        except:
            messages.error(request, 'Please enter your valid address..')

    return render(request, 'account/add_address.html')


def remove_address(request, id):
    address = get_object_or_404(Address, user=request.user, id=id)
    address.delete()
    messages.success(request, "Address removed.")
    return redirect('profile')


def find_locality(request):
    pin_code = request.GET['pin_code']

    url = "https://api.postalpincode.in/pincode/" + str(pin_code)
    response = requests.get(url)
    data = response.json()

    post_offices = data[0]['PostOffice']
    locality = [i['Name'] for i in post_offices]

    locality = render_to_string('partials/_localities.html', {'localities': locality})
    data = {
        'state': data[0]['PostOffice'][0]['State'],
        'district': data[0]['PostOffice'][0]['District'],
        'phone': request.user.phone_number,
        'locality': locality
    }
    return JsonResponse({'data': data})


class ChangePasswordView(PasswordChangeView):
    template_name = 'account/change_password.html'
    form_class = ChangePasswordForm


class ResetPasswordView(PasswordResetView):
    template_name = 'account/password_reset.html'
    form_class = ResetPasswordForm
