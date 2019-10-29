from django.contrib import admin

from .models import Pizza, Topping, Sub, Extra, Salad, Pasta, Dinner_Platter, Order, PizzaOrder, SubOrder

admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(Extra)
admin.site.register(Salad)
admin.site.register(Pasta)
admin.site.register(Dinner_Platter)
admin.site.register(Order)
admin.site.register(PizzaOrder)
admin.site.register(SubOrder)
