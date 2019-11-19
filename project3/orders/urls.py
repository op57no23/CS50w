from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("register", views.registration_view, name = 'register'),
    path("checkout", views.checkout_view, name = 'checkout'),
    path("modal", views.modal_form, name = 'modal_form'),
    path("additem", views.add_item, name = 'additem'),
    path('delete', views.delete_item, name = 'delete'),
    path('place_order', views.place_order, name = 'place_order')
]
