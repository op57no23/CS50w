import pdb
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
    
    def __init__(self, *args, **kwargs):
        super(PizzaModal, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "pizzaForm"

    def set_initial(self, **kwargs):
        sizeArg = kwargs.pop('size')
        idArg = kwargs.pop('id')
        toppingArg = kwargs.pop('topping_number')
        self.fields['size'].initial = sizeArg
        self.fields['id'].initial = idArg
        self.fields['topping_number'].initial = toppingArg
        self.fields['toppings'].label = f'Please select {toppingArg}' 
        if self.fields['topping_number'].initial == 0:
            self.fields['toppings'].widget = forms.HiddenInput()
            self.fields['toppings'].disabled = True

    def clean_toppings(self):
        toppings = self['toppings'].value()
        if (len(toppings) != int(self['topping_number'].value())):
            raise forms.ValidationError('Incorrect number of toppings', code = 'topping_incorrect')
        return self.cleaned_data['toppings']

    topping_number = forms.IntegerField(min_value = 0, max_value = 3, widget = forms.HiddenInput())
    size = forms.ChoiceField(choices = [('small', 'small'), ('large', 'large')], widget = forms.HiddenInput())
    toppings = forms.MultipleChoiceField(required = False, choices = [(topping.id, topping.name) for topping in Topping.objects.all()] + [], widget = forms.CheckboxSelectMultiple)
    quantity = forms.IntegerField(min_value = 0, max_value = 10, initial = 1)
    id = forms.IntegerField(widget = forms.HiddenInput())

class SubModal(forms.Form):
    extras = forms.MultipleChoiceField(label = "Extras: 50 cents each", choices = [(extra.id, extra.name) for extra in Extra.objects.all()], widget = forms.CheckboxSelectMultiple, required = False)
    quantity = forms.IntegerField(min_value = 0, max_value = 10, initial = 1)
    size = forms.ChoiceField(choices = [('small', 'small'), ('large', 'large')], widget = forms.HiddenInput())
    id = forms.IntegerField(widget = forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(SubModal, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "subForm"

    def set_initial(self, **kwargs):
        sizeArg = kwargs.pop('size')
        idArg = kwargs.pop('id')
        self.fields['size'].initial = sizeArg
        self.fields['id'].initial = idArg

class Modal(forms.Form):
    id = forms.IntegerField(widget = forms.HiddenInput())
    quantity = forms.IntegerField(min_value = 0, max_value = 10, initial = 1)
    size = forms.ChoiceField(choices = [('none', 'none'), ('small', 'small'), ('large', 'large')], widget = forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(Modal, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "generalForm"

    def set_initial(self, **kwargs):
        sizeArg = kwargs.pop('size')
        idArg = kwargs.pop('id')
        self.fields['size'].initial = sizeArg
        self.fields['id'].initial = idArg


