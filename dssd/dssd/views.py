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
        "query": '{ countries { code, name, states { name } } }'
    }
    
    headers = {'content-type': 'application/json'}
    response = requests.post('https://countries.trevorblades.com/', json=query, headers=headers)
    return response.json()['data']['countries']

def login_bonita():
    body={'username': 'william.jobs',  'password': 'bpm'}
    headers={"Content-type":"application/x-www-form-urlencoded",'Accept': 'application/json'}
    response = requests.request("POST",'http://localhost:8080/bonita/loginservice',params=body, headers=headers)
   
    #una vez obtenidop el token, obtenemos el id del proceso a usar en este caso Pool3
    cookies = ''
    for key in response.cookies.keys():
        valor = key + '=' + response.cookies[key] + ';'
        cookies+= valor

    return [cookies, response.cookies.get('X-Bonita-API-Token')]

def enviar_formulario(id_sociedad_anonima):
    
    #Obtenemos el token
    proceso = {'s': 'Pool3'}
    cookies, token = login_bonita()
    print(f'1 {cookies}')
    header = {'Cookie': cookies,'Content-Type':'application/json'}
    response = requests.request("GET", 'http://localhost:8080/bonita/API/bpm/process', params= proceso, headers= header)
    id_proceso = response.json()[0]['id']
    print(id_proceso)

    #creamos el case
    header = {'X-Bonita-API-Token': str(token),"cookie":cookies}
    body1='{"processDefinitionId":'+ str(id_proceso) + '}'
    response = requests.request("POST",'http://localhost:8080/bonita/API/bpm/case', headers=header,data=body1) 
    id_caso=response.json()["id"]
    
    #seteamos el valor de la petición para el alta
    body2 = '{"type":"java.lang.String","value": ' + str(id_sociedad_anonima) + '}'
    url=f'http://localhost:8080/bonita/API/bpm/caseVariable/{id_caso}/id_pedido'
    response = requests.request("PUT",url, headers=header,data=body2) 



    

class RegistroSAView(View):
    def get(self,request):
        if not request.user.is_authenticated:
           return redirect('/login/') 
        return render(request,'sociedad_anonima/register.html', context={'countries': get_countries()})

    def post(self,request):
        data = {
            'nombre': request.POST.get('nombre'),
            'porcentajeApoderado': float(request.POST.get('porcentajeApoderado')),
            'estatuto': request.POST.get('estatuo'),
            'domicilio_legal': request.POST.get('domicilio_legal'),
            'domicilio_real': request.POST.get('domicilio_real'),
            'nombre_apoderado': request.POST.get('nombre_apoderado'),
            'apellido_apoderado': request.POST.get('apellido_apoderado'),
            'email_apoderado': request.POST.get('email_apoderado'),
        }
        
        ### Agregamos la info de socios
        nombre_socios = request.POST.getlist('nombre_socio')
        apellido_socios = request.POST.getlist('apellido_socio')
        porcentaje_socios = request.POST.getlist('porcentajeSocio')
        
        socios = []
        for i in range(len(nombre_socios)):
            socios.append({
                'nombre': nombre_socios[i] , 
                'apellido': apellido_socios[i], 
                'porcentaje': float(porcentaje_socios[i])
            })
        data['socios'] = socios
        data['paises'] = request.POST.getlist('countries')
        data['estados'] = request.POST.getlist('states')
    
        sociedad_anonima = repository.add_sociedad_anonima(data)
        enviar_formulario(sociedad_anonima.id)
        return redirect('/')

