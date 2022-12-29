from django.contrib.auth import views as auth_views
from django.urls import path

from account import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='products:home'), name="logout"),
    path('profile/', views.profile, name="profile"),
    path('wishlist/', views.WishlistView.as_view(), name="wishlist"),
    path('add-wishlist/', views.add_to_wishlist, name="add_wishlist"),
    path('remove-wishlist/<str:p_id>/', views.remove_from_wishlist, name="del_wishlist"),
    path('add-address/', views.add_address, name="add_address"),
    path('remove-address/<int:id>/', views.remove_address, name="remove_address"),
    path('ajax/find-locality/', views.find_locality, name="pin_api"),

    path('password-change/', views.ChangePasswordView.as_view(), name="password_change"),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='account/password_change_done.html'), name="password_change_done"),
]
