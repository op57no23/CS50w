from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import RequestContext
from crispy_forms.utils import render_crispy_form
from .models import *
from .forms import LoginForm, RegistrationForm, PizzaModal
import pdb

def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {'form': LoginForm()})
    salads = Salad.objects.all()
    dinner_Platters = Dinner_Platter.objects.all()
    subs = Sub.objects.all()
    pastas = Pasta.objects.all()
    pizzas = Pizza.objects.filter(sicilian = False)
    sicilian = SicilianPizza.objects.all()
    context = {
        'salads': salads,
        'dp': dinner_Platters,
        'subs': subs,
        'pastas': pastas,
        'pizzas': pizzas,
        'sicilian': sicilian,
        "user": request.user
            }
    return render(request, "orders/home.html", context)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "orders/login.html", {'form': form, "message": "Invalid Credentials"})
        context = {
                'form': form
                }
        return render(request, 'orders/login.html', context)
    return HttpResponseRedirect(reverse('index'))

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {'form': LoginForm(), "message": "You have successfully logged out"})

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username = username, password = password, email = email, first_name = first_name, last_name = last_name)
            user.save()
            return HttpResponseRedirect(reverse('index'))
        return render(request, "orders/register.html", {'form': form})
    return render(request, "orders/register.html", {'form': RegistrationForm()})

def checkout_view(request):
    pass
    """
    cart = request.session.get('cart', False)

    if (cart)
        return render(request, "orders/checkout.html", {'cart': cart})
    """

def pizza_form(request):
    if request.method == "GET":
        topping_number = request.GET.get("toppings")
        request_context = RequestContext(request)
        pdb.set_trace()
        return render_crispy_form(PizzaModal(topping_number = topping_number), context = request_context)

