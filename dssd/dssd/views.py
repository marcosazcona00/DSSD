from django.http import *
from django.shortcuts import render 

def home(request):
    return render(request, 'layout.html')