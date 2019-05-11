from django.contrib import admin
from catalog.models import Category, Product, CartItem, Cart, Order, Company

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Company)
# Register your models here.
