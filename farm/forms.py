from django import forms
from .models import UserProfile, Category, Product, LOCATION_CHOICES


class RegistrationForm(forms.ModelForm):
    location = forms.ChoiceField(choices=LOCATION_CHOICES, label='Location')

    class Meta:
        model = UserProfile
        fields = ['username','login', 'password', 'email', 'phone', 'date_of_birth', 'location']
        widgets = {
            'password': forms.PasswordInput(),
        }

class CategoryForm(forms.Form):
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)


class ProductForm(forms.Form):
    products = forms.ModelChoiceField(queryset=Product.objects.none(), empty_label=None)
    quantity = forms.IntegerField(min_value=1)

class OrderConfirmationForm(forms.Form):
    confirm_order = forms.BooleanField(widget=forms.HiddenInput(), initial=True)


