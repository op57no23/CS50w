from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Topping, Extra
from django.core import validators

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'
        self.helper.add_input(Submit('submit', 'Submit'))

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'register'
        self.helper.add_input(Submit('submit', 'Submit'))

class PizzaModal(forms.Form):
    def topping_validator(list_of_items):
        if (len(list_of_items) != topping_number):
            raise ValidationError(_('Incorrect number of toppings'), code = 'topping_incorrect')

    toppings = forms.MultipleChoiceField(validators=[topping_validator], choices = [(topping.id, topping.name) for topping in Topping.objects.all()])
    quantity = forms.IntegerField(min_value = 0, max_value = 10)
    
    def __init__(self, *args, **kwargs):
        topping_number = kwargs.pop('topping_number')
        super(PizzaModal, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'additem'

    
class SubModal(forms.Form):
    extras = forms.MultipleChoiceField(choices = [(extra.id, extra.name) for extra in Extra.objects.all()])
    quantity = forms.IntegerField(min_value = 0, max_value = 10)
    
    def __init__(self, *args, **kwargs):
        super(SubModal, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'additem'




