from django.db import models

class MenuItem(models.Model):
    price = models.FloatField()
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
    sizes = (('S', "Small"), ("L", "Large"))
    size = models.CharField(max_length=5, choices = sizes)
    special = models.BooleanField()
    sicilian = models.BooleanField()

    def __str__(self):
        sicilian_string = ""
        if (self.sicilian):
            sicilian_string = "sicilian"
        return "%s %s -- %s" % (self.name, sicilian_string, self.size)

class PizzaOrder(Pizza):
    topps = models.ManyToManyField(Topping)

    def __str__(self):
        topping_string = ""
        for topp in self.topps.all():
            topping_string += str(topp) + " "

        sicilian_string = ""
        if (self.sicilian):
            sicilian_string = "sicilian"
        return ("%s %s %s with toppings: %s" % (self.size, self.name, sicilian_string, topping_string))


class Sub(MenuItem):
    sizes = (('S', "Small"), ("L", "Large"))
    size = models.CharField(max_length=5, choices = sizes)

    def __str__(self):
        return "%s -- %s" % (self.name, self.size) 

class SubOrder(Sub):
    extras = models.ManyToManyField(Extra)

    def __str__(self):
        extra_string = ""
        for extra in self.extras.all():
            extra_string += str(extra) + ", "
        return "%s %s. Extras: %s" % (self.size, self.name, extra_string) 


class Pasta(MenuItem):
    
    def __str__(self):
        return self.name


class Salad(MenuItem):
    
     def __str__(self):
        return self.name

class Dinner_Platter(MenuItem):
    sizes = (('S', "Small"), ("L", "Large"))
    size = models.CharField(max_length=5, choices = sizes)

    def __str__(self):
        return "%s -- %s" % (self.name, self.size)
