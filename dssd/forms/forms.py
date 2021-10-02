from django import forms
from django.contrib.auth.models import User

class FormularioRegistro(forms.Form):
    email = forms.EmailField(max_length = 254)
    password = forms.CharField(max_length = 20)

class FormularioIniciarSesion(forms.Form):
    email = forms.CharField(max_length=254,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Email",'type':"email"}))
    password = forms.CharField(max_length=254,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Clave",'type':"password"}))