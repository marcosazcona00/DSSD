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
            #login_bonita()
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
    #hay q desplegar la app y el usuario antes de correr esto sino no funca, no basta con solo la app
    body1={'username': 'cristian',  'password': 'bpm'}
    headers={"Content-type":"application/x-www-form-urlencoded",'Accept': 'application/json'}
    response = requests.post('http://localhost:8080/bonita/loginservice',params=body1, headers=headers)
    headers=response.headers
    print('headers',response.headers ,'content', response.content)
    token=(((dict(response.headers)['Set-Cookie'].split(';'))[4].split(','))[1]).split('=')[1]
    print('token',token)
    #intentamos obtener el id del proceso
    headers={'Accept': 'application/json','X-Bonita-API-Token':token}
    parametters={'name':'Pool1'}
    response = requests.post('http://localhost:8080/bonita/API/bpm/process',headers=headers,params=parametters)
    print(response)


    

class RegistroSAView(View):
    def get(self,request):
        return render(request,'sociedad_anonima/register.html', context={'countries': get_countries()})

    def post(self,request):
        # <QueryDict: {'csrfmiddlewaretoken': ['OtcUT4CJfJ5ydLhTB3KTXG6OUNKbDSMS4bYg4zBjB6Yql3uA3beuMtHrqawWBlDw'], 
        # 'nombre': ['.'], 'porcentajeApoderado': ['80'], 'estatuo': ['tokengit.txt'], 'domicilio_legal': ['asd'], 
        # 'domicilio_real': ['asd'], 'nombre_apoderado': ['asd'], 'apellido_apoderado': ['asd'], 
        # 'email_apoderado': ['a@gmail.com'], 'nombre_socio': ['marcos', 'fran'], 'apellido_socio': ['marcos', 'fran'], 
        # 'porcentajeSocio': ['10', '10'], 'countries': ['AT', 'AU']}>
        # [06/Oct/2021 23:53:04] "POST /registro_sa/ HTTP/1.1" 302 0

        data = {
            'nombre': request.POST.get('nombre'),
            'porcentajeApoderado': float(request.POST.get('porcentajeApoderado')),
            'estatuto': request.POST.get('estatuo'),
            'domicilio_legal': request.POST.get('domicilio_legal'),
            'domicilio_real': request.POST.get('domicilio_real'),
            'email_apoderado': request.POST.get('email_apoderado'),
        }
        
        ### Agregamos la info de socios
        nombre_socios = request.POST.getlist('nombre_socio')
        apellido_socios = request.POST.getlist('apellido_socio')
        porcentaje_socios = request.POST.getlist('porcentajeSocio')
        
        socios = []
        for i in range(len(nombre_socios)):
            print(nombre_socios[i])
            socios.append({
                'nombre': nombre_socios[i] , 
                'apellido': apellido_socios[i], 
                'porcentaje': float(porcentaje_socios[i])
            })
        data['socios'] = socios
        data['paises'] = request.POST.getlist('countries')
    
        ok = repository.add_sociedad_anonima(data)
        return redirect('/')

