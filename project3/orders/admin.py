from django.contrib import admin

from .models import Topping, Extra, Order, MenuItem, OrderItem

admin.site.register(OrderItem)
admin.site.register(MenuItem)
admin.site.register(Topping)
admin.site.register(Extra)
admin.site.register(Order)
