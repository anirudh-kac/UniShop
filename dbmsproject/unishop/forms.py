from django import forms
from .models import User , UserProfile , Shop ,Product


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username","email","password"]


class UserProfileForm(forms.ModelForm):

    class Meta :
        model = UserProfile
        exclude = ["user","dob"]

class ShopForm(forms.ModelForm):

    class Meta:
        model = Shop
        exclude = ["owner","image_url"]


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['brand','name','price','quantity']