from django.shortcuts import render, HttpResponse


#from Peliculas.models import Sesiones

# Create your views here.

def home(request):

    return render(request, "Eventiket/home.html")








