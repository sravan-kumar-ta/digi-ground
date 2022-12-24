from django.contrib.auth import views as auth_views
from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='products:home'), name="logout"),
]
