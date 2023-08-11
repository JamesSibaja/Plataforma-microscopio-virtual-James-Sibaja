from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views import generic
from django.template import Template, context
from django.views.generic.edit import FormView, DeleteView
from django.db.models import Q
from Projects.forms import NoteForm, ProjectForm, SearchForm, ProjectSlideForm
from Projects.models import Project, Notes, ProjectSlide
from Microscopio.models import Slide
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your views here.

class projects(generic.ListView,FormView,):
    template_name = "Projects/projectList.html"
    model = Project
    form_class = ProjectForm
    paginate_by = 12
    
    def get_queryset(self):
        qs = super(projects, self).get_queryset()
        queryset2 = self.request.GET.get('buscar')
        usuario = self.request.user
        queryset = usuario.sharedUsers.all()
        # queryset = qs.filter(user=self.request.user)
        

        if queryset2:
        
            palabras = queryset2.split()
            condiciones_busqueda = []

            for palabra in palabras:
                condicion = Q(name__icontains=palabra)
                condicion2 = Q(description__icontains=palabra) 
                condiciones_busqueda.append(condicion)
                condiciones_busqueda.append(condicion2)

            consulta = Q()
            for condicion in condiciones_busqueda:
                consulta |= condicion
            queryset = queryset.filter(consulta)

        return queryset



    def get_success_url(self):
        return self.request.path

    def get_context_data(self,**kwargs):
        context = super(projects, self).get_context_data(**kwargs)
        context['form'] = ProjectForm
        context['slideSel'] = None
        if self.request.path != '/project/':
            object_instance = Slide.objects.filter(id=self.kwargs['slideId'])
            for slide in object_instance:
                context['slideSel'] = slide
                context['make'] = True
        return context

    def post(self, request, *args, **kwargs):
        object_instance = request.user
        form = ProjectForm(request.POST)
        # print('jos')
        if form.is_valid():
            # mySlides = Slide.objects.filter(name=request.POST.get('slide', ''))
            print(request.POST.get('slide', ''))
            # for slide in mySlides:
                # mySlide = slide
            instancia = form.save(commit=False)
            instancia.user = object_instance
            
            # instancia.slide = mySlide
            instancia.save()

        return redirect(self.request.path)

class projectSlideDetail(generic.DetailView,FormView,DeleteView):
    # note = Notes.objects.all()
    template_name = "Projects/projectSlide.html"
    model = ProjectSlide
    form_class = ProjectSlideForm
     

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(projectSlideDetail, self).get_context_data(**kwargs)
        context['projectSlide'] = self.get_object()
        context['plates'] = ProjectSlide.objects.filter(project=context['projectSlide'].project)
        context['apuntes'] = Notes.objects.filter(project=context['projectSlide'])
        context['notes']=None
        context['form'] = NoteForm
        # context['notes'] = apuntes
        return context

    def post(self, request, *args, **kwargs):
        object_instance = self.get_object()
        form = NoteForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.project = object_instance
            instancia.xUnoPos = 1
            instancia.yUnoPos = 1
            instancia.xDosPos = 2
            instancia.yDosPos = 2
            instancia.geojson_data = [1]
            instancia.save()
        return FormView.post(self, request, *args, **kwargs)
    
class projectDetail(generic.DetailView,FormView,DeleteView):
    # note = Notes.objects.all()
    template_name = "Projects/project.html"
    model = Project
    form_class = ProjectSlideForm
    
     

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(projectDetail, self).get_context_data(**kwargs)
        projectSelf =  self.get_object()
        placas = ProjectSlide.objects.filter(project=projectSelf.project)
        catalogo = Slide.objects.all()
        idNum = self.kwargs['map']
        usuarios = projectSelf.sharedUsers
        #pk = ProjectSlide.objects.filter(project=context['pk'])
        context['form'] = ProjectSlideForm
        context['plates'] = placas
        context['catalogo'] = catalogo
        context['usuarios'] = usuarios
        
        context['slideSel'] = None
        context['slideId'] = None
        # context['make'] = str(self.kwargs['sel'])
        context['pk'] = str(self.kwargs['pk'])
      
        return context
    
    def get(self, request, *args, **kwargs):
        # context = super(projectDetail, self).get_context_data(**kwargs)
        
        form = ProjectSlideForm
        project = self.get_object()
        plates  = ProjectSlide.objects.filter(project=self.get_object())
        
        pk = str(self.kwargs['pk'])
        queryset = request.GET.get('buscar')
        ver = request.GET.get('ver')
        numUser = 0
        for item in project.sharedUsers.all():
            numUser = numUser + 1

        numPlacas = 0
        for item in plates:
            numPlacas = numPlacas + 1


        mapNum = self.kwargs['map']
        optionNum = self.kwargs['option']
        mapSlide = None
        if(optionNum ==1):
            if(mapNum):
                mapSlide = ProjectSlide.objects.get(id=mapNum)
                projec_slide_instance = ProjectSlide.objects.get(id= mapNum )
                form = ProjectSlideForm(instance=projec_slide_instance)

        if(optionNum ==2):
                mapSlide = Slide.objects.get(id=mapNum)
        placaID = request.GET.get('placaId')
        catalogo = Slide.objects.all()
        mySlide = None
        slideName = None

        if placaID:
            mySlide = Slide.objects.get(id=placaID)
            slideName = mySlide.name
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
        return render(request,"Projects/project.html",{'catalogo':catalogo,'numPlacas':numPlacas,'numUser':numUser,'optionNum':optionNum,'mapSlide':mapSlide,'project':project,'ver':ver,'form':form,'pk':pk,'placaId':placaID,'slideName':slideName,'plates':plates})
    
    
    def post(self, request, *args, **kwargs):
        object_instance = self.get_object() 
        idNum = self.kwargs['map']
        optionNum = self.kwargs['option']
        if(optionNum == 1):
            projec_slide_instance = ProjectSlide.objects.get(id= idNum )
            form = ProjectSlideForm(request.POST,instance=projec_slide_instance)
        else:
            form = ProjectSlideForm(request.POST)
        # print('jos')
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.project = object_instance
            # instancia.placaId = request.POST.get('placaId')
            mySlide = Slide.objects.get(id=request.POST.get('slide'))
            # mySlide = None
            # # print(request.POST.get('slide', ''))
            # for slide in mySlides:
            #     mySlide = slide
            # instancia.user = object_instance
            instancia.slide = mySlide
            instancia.save()

        return redirect(self.request.path)

class noteDetail(generic.DetailView):
    # note = Notes.objects.all()
    template_name = "Projects/note.html"
    model = Notes
    

    def get_context_data(self, *args, **kwargs):
        context = super(noteDetail, self).get_context_data(**kwargs)
        apuntes = Notes.objects.filter(project=context['notes'].project)
        context['apuntes'] = apuntes
        return context
    

def obtener_lista(request):
    # Aquí debes obtener la lista actualizada desde tu modelo o cualquier otra fuente de datos
    lista_actualizada = Notes.objects.all().values()  # Por ejemplo, obtenemos todos los objetos del modelo y los convertimos a diccionario

    # Devuelve los datos en formato JSON
    return JsonResponse(list(lista_actualizada), safe=False)

def delete(request, nota_id):
    instancia = Notes.objects.get(id=nota_id)
    new_url = '/projectSlideDetail/'+str(instancia.project.id)
    instancia.delete()

    return redirect(new_url)


def deleteProject(request, project_id):
    instancia = Project.objects.get(id=project_id)
    new_url = 'project-list'
    instancia.delete()

    return redirect(new_url)

def deleteProjectSlide(request, project_id):
    instancia = ProjectSlide.objects.get(id=project_id)
    new_url = instancia.project.get_absolute_url()
    instancia.delete()

    return redirect(new_url)

def deleteProjectUser(request, project_id,projectUser_id):
    usuario = User.objects.get(id=projectUser_id)
    proyecto = Project.objects.get(id=project_id)
    proyecto.sharedUsers.remove(usuario)
    
    new_url = '/projectDetail/'+str(project_id)+'/3/0'

    return redirect(new_url)

def newProjectUser(request, project_id,projectUser_id):

    usuario = User.objects.get(id=projectUser_id)
    proyecto = Project.objects.get(id=project_id)
    proyecto.sharedUsers.add(usuario)
    new_url = '/projectDetail/'+str(project_id)+'/3/0'

    return redirect(new_url)

def datos_actualizados_catalogo(request,*args, **kwargs):
    

    queryset = kwargs.get('buscar', None)
    items = Slide.objects.all() 
    if queryset and not queryset == '_':
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

        items = Slide.objects.filter(consulta)
        
    paginator = Paginator(items,9)
    
    page = request.GET.get('page')
        
        
    items= paginator.get_page(page)
    
    nombres = [item.name for item in items]
    idList = [item.id for item in items]
    imagenes = [item.image.url for item in items]
    descripcion = [item.description for item in items]

    return JsonResponse({'name':nombres,'id':idList,'image':imagenes,'description':descripcion}, safe=False)  

def datos_actualizados_placas(request,*args, **kwargs):

    project= kwargs.get('project', None)
    items =  ProjectSlide.objects.filter(project = project) 
    queryset = kwargs.get('buscar', None)
    if queryset and not queryset == '_':
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
        
        consulta &= Q(project = project)

        items =  ProjectSlide.objects.filter(consulta)
        
    paginator = Paginator(items,9)
    
    page = request.GET.get('page')
        
        
    items= paginator.get_page(page)
    nombres = [item.name for item in items]
    idList = [item.id for item in items]
    
    return JsonResponse({'name':nombres,'id':idList}, safe=False)  

def datos_actualizados_colaboradores(request,*args, **kwargs):
    queryset = kwargs.get('buscar', None)
    itemsBuscar = None
    nombresBuscar = None
    idListBuscar = None
    if queryset and not queryset == '_':
        palabras = queryset.split()
        condiciones_busqueda = []

        for palabra in palabras:
            condicion = Q(username__icontains=palabra)
            # condicion2 = Q(description__icontains=palabra) 
            condiciones_busqueda.append(condicion)
            # condiciones_busqueda.append(condicion2)

        consulta = Q()
        for condicion in condiciones_busqueda:
            consulta |= condicion

        itemsBuscar = User.objects.filter(consulta)
        
        paginator = Paginator(itemsBuscar,9)    
        page = request.GET.get('page')
        itemsBuscar= paginator.get_page(page)
        nombresBuscar = [item.username for item in itemsBuscar]
        idListBuscar = [item.id for item in itemsBuscar]
    
    project= kwargs.get('project', None)
    list = Project.objects.get(id = project)
    items = list.sharedUsers.all()
    nombres = [item.username for item in items]
    idList = [item.id for item in items]
    ownerID = list.user.id
    ownerN = list.user.username

    return JsonResponse({'name':nombres,'id':idList,'ownerN':ownerN,'ownerID':ownerID,'nameS':nombresBuscar,'idS':idListBuscar}, safe=False)  