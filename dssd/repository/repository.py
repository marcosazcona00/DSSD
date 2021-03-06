from datetime import date
from models.models import *
from django.contrib.auth.models import User

class Repository(object):
    def find_user_by_email(self, email):
        users_filtered = User.objects.filter(username = email)
        return users_filtered[0] if len(users_filtered) > 0 else None

    def add_user(self, email, password):
        if not self.find_user_by_email(email):
            user = User.objects.create_user(username = email, password = password)
            return True
        return False

    def create_apoderado(self, nombre, apellido, porcentaje):
        apoderado =  SocioSociedadAnonima(nombre = nombre,apellido = apellido,porcentaje_aporte = porcentaje)
        apoderado.save()
        return apoderado

    def findPiasByCodigGQL(self,codigo_gql):
        paises_filtered = Pais.objects.filter(codigo_gql=codigo_gql)
        return paises_filtered[0] if len(paises_filtered) > 0 else None    

    def create_pais(self, codigo_gql):
        pais = self.findPiasByCodigGQL(codigo_gql)
        if pais:
           return pais
        pais = Pais(codigo_gql = codigo_gql)
        pais.save()
        return pais
    
    def findEstadoByNameGQL(self,nombre_gql):
        estados_filtered = Estado.objects.filter(nombre_gql=nombre_gql)
        return estados_filtered[0] if len(estados_filtered) > 0 else None    

    def create_estado(self, nombre_gql, code_pais_gql):
        estado = self.findEstadoByNameGQL(nombre_gql)
        if estado:
            return estado
        estado = Estado(nombre_gql = nombre_gql, pais_gql = code_pais_gql)
        estado.save()
        return estado

    def add_sociedad_anonima(self, data):
        apoderado = self.create_apoderado(nombre = data['nombre_apoderado'], 
                    apellido = data['apellido_apoderado'], porcentaje = data['porcentajeApoderado'])

        sociedad_anonima = SociedadAnonima(nombre = data['nombre'],fecha_creacion = date.today() ,estatuto = data['estatuto'],
                        domicilio_real=data['domicilio_real'],domicilio_legal=data['domicilio_legal'],email_apoderado=data['email_apoderado'],
                        apoderado = apoderado)
        sociedad_anonima.save()

        if(len(data['paises'])== 0):
            # Si no vienen paises, por defecto definimos a argentina
            pais = self.create_pais("AR")
            sociedad_anonima.paises_exporta.add(pais)
        else:
            for codigo_pais in data['paises']:
                pais = self.create_pais(codigo_pais)
                sociedad_anonima.paises_exporta.add(pais)
        
        # Agregamos los estados a los que se exporta en la bd
        for estado in data['estados']:
            nombre_estado_gql = estado.split(':')[0]
            code_pais_gql = estado.split(':')[1]
            estado = self.create_estado(nombre_estado_gql,code_pais_gql)
            sociedad_anonima.estados_exporta.add(estado)
            
        for socio in data['socios']:
            socio = self.create_apoderado(nombre = socio['nombre'], apellido = socio['apellido'], porcentaje = socio['porcentaje'])
            socio.sociedad = sociedad_anonima
            socio.save()

        return sociedad_anonima