from django import forms
from .models import User , UserProfile , Store ,Product


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username","email","password"]


class UserProfileForm(forms.ModelForm):

    class Meta :
        model = UserProfile
        exclude = ["user","dob"]

class StoreForm(forms.ModelForm):

    class Meta:
        model = Store
        exclude = ["owner"]


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['brand','name','price','quantity']