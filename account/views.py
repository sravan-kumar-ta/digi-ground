from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from account.CustomBackend import CustomAuth
from account.forms import CustomUserCreationForm, LoginForm
from account.models import CustomUser
from products.models import Product, Cart


class RegistrationView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "account/register.html"
    success_url = reverse_lazy("account:login")


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
                # return redirect('account:login')
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
            messages.success(self.request, 'Successfully logged in')
            return redirect('products:home')
        else:
            messages.error(self.request, "Invalid credentials..!")
            return redirect('account:login')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Credentials')
        return redirect('account:login')
