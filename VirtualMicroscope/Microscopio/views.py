from django.shortcuts import render
from Microscopio.models import Slide
from django.views.generic import CreateView
from django.views import generic
from django.template import Template, context
from django.db.models import Q, Count
from django.core.paginator import Paginator

# Create your views here.

class micro(generic.DetailView):
    template_name = "Microscopio/microscopio.html"
    model = Slide

class microfull(generic.DetailView):
    template_name = "Microscopio/microscopiofull.html"
    model = Slide

def catalogo(request):
    queryset = request.GET.get('buscar')
    ver = request.GET.get('ver')
    catalogo = Slide.objects.all()
    
    if queryset:
        palabras = queryset.split()
        condiciones_busqueda = []

        for palabra in palabras:
            condicion = Q(name__icontains=palabra)
            condicion2 = Q(description__icontains=palabra) 
            condiciones_busqueda.append(condicion)
            condiciones_busqueda.append(condicion2)

        consulta = Q()
        for condicion in condiciones_busqueda:
            consulta |= condicion

        catalogo = Slide.objects.filter(consulta)
        
    paginator = Paginator(catalogo,30)

    if ver:
        paginator = Paginator(catalogo,9)
    
    page = request.GET.get('page')
    catalogo = paginator.get_page(page)

    return render(request,"Microscopio/catalogo.html",{'catalogo':catalogo,'ver':ver})
