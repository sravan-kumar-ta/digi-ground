from django.contrib import admin
from products.models import Category


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug')


admin.site.register(Category, CategoryAdmin)
