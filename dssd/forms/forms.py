from django import forms
from django.contrib.auth.models import User

class FormularioRegistro(forms.Form):
    def __init__(self,*args,**kwargs):
        super(FormularioRegistro,self).__init__(*args,**kwargs)

    Email = forms.EmailField(max_length = 254, widget=forms.TextInput(attrs={'class':'form-control'}))
    Contrasena = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),max_length = 20)

    def clean_Email(self):
        email = self.cleaned_data['Email']
        if (User.objects.values('username').filter(username = email).exists()):
            raise forms.ValidationError('El Email ya esta registrado en el sistema')
        return email



class FormularioIniciarSesion(forms.Form):
    email = forms.CharField(max_length=254,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Email",'type':"email"}))
    password = forms.CharField(max_length=254,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Clave",'type':"password"}))