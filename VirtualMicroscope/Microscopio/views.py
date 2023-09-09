from django.shortcuts import render
from Microscopio.models import Slide,OpenSlide
from django.views.generic import CreateView
from django.views import generic
from django.template import Template, context
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import  UploadFileForm, SlideForm
from .tasks import convert_to_tiles
from django.http import JsonResponse

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
    catalogo = Slide.objects.filter( assembled=True)
    
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

# class FileUploadView(FormView):
#     template_name = 'Microscopio/subir_archivo.html'
#     form_class = FileUploadForm
#     success_url = '/subir-archivo/'  # Cambia esto a la URL a la que deseas redirigir después de subir el archivo

#     def form_valid(self, form):
#         # Aquí puedes agregar la lógica para manejar el archivo subido, por ejemplo, guardarlo en el servidor
#         return super().form_valid(form)
    
# from django.shortcuts import render
# from .models import Archivo


# def subir_archivo(request):

#     if request.method == 'POST':
#         form = SlideForm(request.POST, request.FILES) 
#         if form.is_valid():
#             instancia = form.save(commit=False)
#             instancia.image = 'archivo/' + instancia.name
#             instancia.path = 'media/slide/slide' +str(instancia.id)
#             instancia.save()
#             archivo = request.FILES['file']


#             with open('media/archivo/' + instancia.name + str(instancia.id), 'wb') as destino:
#                 for chunk in archivo.chunks():
#                     destino.write(chunk)
        
        
#             convert_to_tiles.delay('media/archivo/' +instancia.name + str(instancia.id),'media/slide/slide' +str(instancia.id))
#             return render(request, 'Microscopio/subir_archivo.html', {'archivo_subido': True,'form':form})
#     else:
#         form = SlideForm() 

#     return render(request, 'Microscopio/subir_archivo.html', {'archivo_subido': False,'form':form})

def upload_file(request):
    listSlide = OpenSlide.objects.filter( assembled=False)


    if request.method == 'POST':
        option = int(request.POST.get('option'))
        if(option == 1):
            # form = UploadFileForm(request.POST, request.FILES)
            # if form.is_valid():
            uploaded_file = request.FILES['file']
            # name = form.cleaned_data['name']
            name = uploaded_file.name + '_' + str(OpenSlide.objects.count())
            # description = form.cleaned_data['description']
             # name = form.cleaned_data['name']
            
            
            # if Slide.objects.filter(name=name).exists():
            #     return JsonResponse({'error': 'Ya existe una instancia con este nombre'})
            
            # Crear una instancia del modelo
            instance = OpenSlide(name=name)
            instance.save()
            # instance.image = 'slides/slide' +str(instance.id)+'/1/0/0.jpg'
            instance.path = 'media/archivo/' +str(instance.id)
            # instance.zoomI = 0
            # instance.zoomM = 9
            instance.save()

            with open('media/archivo/' +str(instance.id), 'wb') as destino:
                for chunk in uploaded_file.chunks():
                    destino.write(chunk)
        
        
            # num = convert_to_tiles.delay('media/archivo/' + str(instance.id),'media/slides/slide' +str(instance.id))
            
            response_data = {'message': 'Archivo cargado y procesado exitosamente'}
            return JsonResponse(response_data)
            # else:
        #     return JsonResponse(form.errors, status=400)  # Devuelve errores de validación
        else:
            form = SlideForm(request.POST, request.FILES)
            if form.is_valid():
                option = int(request.POST.get('option'))
                rawSlide = OpenSlide.objects.get(id=int(request.POST.get('slide')))
                instance = form.save(commit=False)
                instance.save()
                instance.rawSlide = rawSlide
                instance.image = 'slides/slide' +str(instance.id)+'/1/0/0.jpg'
                instance.path = 'slide' +str(instance.id)
                instance.save()
                # description = form.cleaned_data['description']
                # name = form.cleaned_data['name']

                convert_to_tiles.delay('media/archivo/' + str(instance.rawSlide.id),'media/slides/slide' +str(instance.id),instance.rawSlide.id,instance.id)
            else:
                return JsonResponse(form.errors, status=400)  # Devuelve errores de validación

    else:
        form = SlideForm()

    return render(request, 'Microscopio/subir_archivo.html', {'form':form,'listSlide':listSlide})