from django.contrib import admin
from products.models import *


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug')


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'brand', 'category', 'price', 'stock')
    list_editable = ('price', 'stock')


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
