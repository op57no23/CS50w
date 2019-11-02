from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("register", views.registration_view, name = 'register'),
    path("checkout", views.checkout_view, name = 'checkout'),
    path("pizza", views.pizza_form, name = 'pizza_form')
]
