from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal info'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'username'
                ),
            },
        ),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
    )

    list_display = ('username', 'email', 'phone_number', 'is_active', 'is_staff')
    filter_horizontal = ()
    list_filter = ()


admin.site.register(get_user_model(), CustomUserAdmin)
