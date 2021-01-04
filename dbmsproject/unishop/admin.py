from django.contrib import admin
from .models import Shop,Product,CartItem,Bill,UserProfile
# Register your models here.

admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Bill)
admin.site.register(UserProfile)
