from dataclasses import field
import imp
from django.forms import ModelForm
from django import forms
from website.models import Product


class UploadProduct(ModelForm):
    title = forms.CharField()
    long_description = forms.TextInput()
    productImage = forms.ImageField()
    price = forms.JSONField()

    class Meta:
        model = Product
        fields = ['title', 'long_description', 'productImage', 'price']
