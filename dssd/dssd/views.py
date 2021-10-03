import json

from django.http import *
from django.views import View

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import requests

from forms.forms import *
from django.views.decorators.csrf import csrf_exempt

from repository.repository import Repository

repository = Repository()

def home(request):
    return render(request, 'layout.html')

def logout_view(request):
    logout(request)
    return redirect('/')

class VistaRegistro(View):   
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'user/register.html')

    @csrf_exempt
    def post(self, request):
        context = {"error": "El formato de los datos ingresados son incorrectos"}
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            saved = repository.add_user(email = request.POST.get("email"), password = request.POST.get("password"))
            if saved:
                return redirect('/')
            context['error'] = "El usuario ya existe"
        return render(request, 'user/register.html', context)

class LoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/alta_formulario')
        return render(request, 'user/login.html')
    
    @csrf_exempt
    def post(self,request):
        user = authenticate(username = request.POST.get("email"), password = request.POST.get("password"))
        if user is not None:
            login(request, user)
            return redirect('/')
        return render(request, 'user/login.html', {"error": "Los datos ingresados son incorrectos"})


def get_countries():
    query = {
        "query": '{ countries { code, name } }'
    }
    
    headers = {'content-type': 'application/json'}
    response = requests.post('https://countries.trevorblades.com/', json=query, headers=headers)
    return response.json()['data']['countries']

def login_bonita():
    body={'username': chessi, 'password': bpm, 'redirect': 'false'}
    headers={"Content-type":"application/x-www-form-urlencoded"}
    response = requests.post('http://localhost:8080/bonita/loginservice',body=body, headers=headers)
    print(response.json()['X-Bonita-API-Token'])

class RegistroSAView(View):
    def get(self,request):
        return render(request,'sociedad_anonima/register.html', context={'countries': get_countries()})

    def post(self,request):
        print(request.POST)
        return redirect('/')

