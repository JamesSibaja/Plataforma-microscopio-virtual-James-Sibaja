from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, CreateUserForm
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,"VMapp/index.html")

class Login(FormView):
    template_name = "VMapp/login.html"
    form_class = LoginForm
    success_url = reverse_lazy ('project-list')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args, **kwargs)

    def form_valid(self,form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

class SignUp(generic.CreateView):
    template_name = "VMapp/signup.html"
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy ('Login')

    def form_valid(self,form):
        return super(SignUp,self).form_valid(form)
    
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            user_profile = request.user.userprofile

            if 'profile_image' in request.FILES:
                profile_image = request.FILES['profile_image']
                user_profile.profile_image = profile_image

        # Puedes guardar otros campos del UserProfile aquí

            user_profile.save()
            # new_password = form.cleaned_data.get('new_password1')
            # if new_password:
            #     user.set_password(new_password)
            user.save()
            return redirect('/project/')
            # Realiza acciones adicionales si es necesario
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'VMapp/edit_profile.html', {'form': form})


