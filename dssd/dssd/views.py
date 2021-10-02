from django.http import *
from django.views import View

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'layout.html')

def logout_view(request):
    logout(request)
    return redirect('/')
   
class LoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/alta_formulario')
        return render(request, 'user/login.html')
    
    def post(self,request):
        es_valido = True 
        if es_valido:
            user = authenticate(username = request.POST.get("email"), password = request.POST.get("password"))
            if user is not None:
                login(request, user)
                return redirect('/')
        return render(request, 'user/login.html', {"error": "Los datos ingresados son incorrectos"})

