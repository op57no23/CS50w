from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from .models import MenuItem, OrderItem, Order, Extra, Topping
from .forms import LoginForm, RegistrationForm, PizzaModal, SubModal, Modal
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import pdb
import re
import json

@ensure_csrf_cookie
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {'form': LoginForm()})
    pdb.set_trace()
    try:
        order = Order.objects.filter(user = request.user.id)[0]
    except:
        order = ""
    salads = MenuItem.objects.filter(type = 'Salad')
    dinner_Platters = MenuItem.objects.filter(type = 'DP')
    subs = MenuItem.objects.filter(type = 'Sub')
    pastas = MenuItem.objects.filter(type = 'Pasta')
    pizzas = MenuItem.objects.filter(type = 'Pizza')
    sicilian = MenuItem.objects.filter(type = 'SP')
    context = {
            'order': order,
            'salads': salads,
            'dp': dinner_Platters,
            'subs': subs,
            'pastas': pastas,
            'pizzas': pizzas,
            'sicilian': sicilian,
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
                request.session['cart'] = []
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
    cart = json.loads(json.loads(request.POST['cart'])['cart'])
    if (Order.objects.filter(user = User.objects.get(pk=request.user.id), completed = False)):
        order = Order.objects.filter(user = User.objects.get(pk=request.user.id), checked_out = False))[0]
    else:
        order = Order(user = Users.objects.get(pk = request.user.id))
        order.save()
    total = 0
    items = []
    for item in cart:
        currentItem = {}
        if 'toppings' in item:
            orderItem = OrderItem(price = 0, menuItem = MenuItem.objects.get(pk = item['id']), quantity = item['quantity'], size = item['size'])
            orderItem.save()
            for topping in item['toppings']:
                orderItem.toppings.add(Topping.objects.get(pk = int(topping)))
            currentItem['additionals'] = orderItem.toppings.all()
        elif 'extras' in item:
            orderItem = OrderItem(price = 0, menuItem = MenuItem.objects.get(pk = item['id']), quantity = item['quantity'], size = item['size'])
            orderItem.save()
            for extra in item['extras']:
                orderItem.extras.add(Extra.objects.get(pk = int(extra)))
                orderItem.price += .50
                total += .50
            currentItem['additionals'] = orderItem.extras.all()
        else:
           orderItem = OrderItem(price = 0, menuItem = MenuItem.objects.get(pk = item['id']), quantity = item['quantity'], size = item['size'])
           orderItem.save()
           currentItem['additionals'] = []
        order.items.add(orderItem)
        if item['size'] == 'small':
            total += orderItem.menuItem.small_price * item['quantity']
            orderItem.price += orderItem.menuItem.small_price
            orderItem.save()
        elif item['size'] == 'large':
            total += orderItem.menuItem.large_price * item['quantity']
            orderItem.price += orderItem.menuItem.large_price
            orderItem.save()
        else:
            total += orderItem.menuItem.price * item['quantity']
            orderItem.price += orderItem.menuItem.price
            orderItem.save()
        currentItem['name'] = orderItem.menuItem.get_type_display() + ": " + orderItem.menuItem.name
        currentItem['size'] = orderItem.size
        currentItem['quantity'] = orderItem.quantity
        currentItem['price'] = orderItem.price * orderItem.quantity
        currentItem['id'] = orderItem.id
        items.append(currentItem)
    return render(request, "orders/checkout.html", {'items': items, 'total': total})

def modal_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        type = request.POST.get("type")
        id = int(re.findall(r'(\d*)_?', request.POST.get("id"))[0])
        if type in ['Sub', 'Pizza', 'Dinner Platter']:
            size = re.findall(r'_(.*)', request.POST.get("id"))[0]
            if type == 'Pizza':
                try:
                    topping_number = int(name[0])
                except:
                    topping_number = 0
                form = PizzaModal()
                form.set_initial(size = size, id = id, topping_number = topping_number)
            elif (type == 'Sub'):
                form = SubModal()
                form.set_initial(size = size, id = id)
            else:
                form = Modal()
                form.set_initial(size = size, id = id)
        else:
            form = Modal()
            form.set_initial(size = 'none', id = id)
        ctx = {'name': name, 'form': form, 'id': id}
        return render(request, 'orders/modalForm.html', context = ctx)

def add_item(request):
    if request.POST.get('form_type') == 'pizzaForm':
        form = PizzaModal(request.POST or None)
    elif request.POST.get('form_type') == 'subForm':
        form = SubModal(request.POST or None)
    else:
        form = Modal(request.POST or None)
    if form.is_valid():
        return JsonResponse({'success': True, 'valid_form': json.dumps(form.cleaned_data)}) 
    ctx = {}
    ctx.update(csrf(request))
    form_html = render_crispy_form(form, context = ctx)
    return JsonResponse({'success': False, 'form_html': form_html})
