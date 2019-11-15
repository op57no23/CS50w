from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    type = models.CharField(max_length=50, choices = [('Pizza', "Pizza"), ('SP', "Sicilian Pizza"), ('Salad', 'Salad'), ('Pasta', 'Pasta'), ('DP', 'Dinner Platter'), ('Sub', 'Sub')], default = 'Sub')
    price = models.FloatField(blank = True, null = True)
    name = models.CharField(max_length=50)
    small_price = models.FloatField(blank = True, null = True)
    large_price = models.FloatField(blank = True, null = True)
    
    def __str__(self):
        return f"{self.type}: {self.name}"

class Topping(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Extra(models.Model):
    name = models.CharField(max_length=50)
    price = .5

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    menuItem = models.ForeignKey(MenuItem, on_delete = models.CASCADE)
    size = models.CharField(max_length=50, choices = [('none', 'none'), ('SM', 'small'), ('LG', 'large')])
    toppings = models.ManyToManyField(Topping)
    extras = models.ManyToManyField(Extra)
    quantity = models.IntegerField()
    price = models.FloatField(null = True)

    def __str__(self):
        if (self.size in [2, 3]):
            if (self.toppings):
                return f"{self.menuItem.get_type_display()}: {self.get_size_display()} {self.menuItem.name} with {self.toppings}"
            elif (self.extras):
                return f"{self.menuItem.get_type_display()}: {self.get_size_display()} {self.menuItem.name} with {self.extras}"
            else:
                return f"{self.menuItem.get_type_display()}: {self.get_size_display()} {self.menuItem.name}"
        else:
                return f"{self.menuItem.get_type_display()}: {self.menuItem.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = 2, null = True) 
    items = models.ManyToManyField(OrderItem)
    completed = models.BooleanField(default = False)
    checked_out = models.BooleanField(default = False)

    def __str__(self):
        output = ""
        for item in self.items.all():
            output += str(item) + "\n"
        return output


