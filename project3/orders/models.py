from django.db import models

class MenuItem(models.Model):
    price = models.FloatField(null = True, blank = True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Topping(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Extra(models.Model):
    name = models.CharField(max_length=50)
    price = .5

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(MenuItem)

    def __str__(self):
        output = ""
        for item in self.items.all():
            output += str(item) + "\n"
        return output

class Pizza(MenuItem):
    sicilian = models.BooleanField(default = False)
    small_price = models.FloatField(default = 10)
    large_price = models.FloatField(default = 10)

class SicilianPizza(Pizza):
    sicilian = True

    def __str__(self):
        return "Sicilian " + self.name

class PizzaOrder(Pizza):
    topps = models.ManyToManyField(Topping)

    def __str__(self):
        topping_string = ""
        for topp in self.topps.all():
            topping_string += str(topp) + " "

        sicilian_string = ""
        if (self.sicilian):
            sicilian_string = "sicilian"
        return ("%s %s with toppings: %s" % (self.name, sicilian_string, topping_string))


class Sub(MenuItem):
    small_price = models.FloatField(null = True, blank = True, default = 6.50)
    large_price = models.FloatField(default = 7.95)


class SubOrder(Sub):
    extras = models.ManyToManyField(Extra)

    def __str__(self):
        extra_string = ""
        for extra in self.extras.all():
            extra_string += str(extra) + ", "
        return "%s. Extras: %s" % (self.name, extra_string)


class Pasta(MenuItem):
    pass

class Salad(MenuItem):
    pass

class Dinner_Platter(MenuItem):
    small_price = models.FloatField(default = 10)
    large_price = models.FloatField(default = 10)
