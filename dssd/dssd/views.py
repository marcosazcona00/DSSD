from django.http import *
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, FileResponse
from django.http import HttpResponseRedirect
from forms.forms import *
from django.views.decorators.csrf import csrf_exempt


class Vista_Registro(View):
    def __init__(self, *args, **kwargs):
        self.contexto = dict()
        super(Vista_Registro, self).__init__(*args, **kwargs)
   
    def get(self, request):
        formulario = FormularioRegistro()
        self.contexto['formulario'] = formulario
        return render(request, 'user/registro.html', self.contexto)

    def __cargar_usuario_suscriptor(self, formulario):
        """
            Carga los datos del suscriptor en la tabla modelos_suscriptor, modelos_usuario y auth_user
        """
        email = formulario.cleaned_data['Email']
        contrasena = formulario.cleaned_data['Contrasena']
        # Cargamos el modelos User de auth_user
        model_usuario = User.objects.create_user(username=email, password=contrasena)  # Se guarda en la tabla auth_user
        model_usuario.save()
        
    @csrf_exempt
    def post(self, request):
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            self.__cargar_usuario_suscriptor(formulario)
            return redirect('/')
        self.contexto['formulario'] = formulario
        return render(request, 'user/registro.html', self.contexto)



def home(request):
    return render(request, 'layout.html')