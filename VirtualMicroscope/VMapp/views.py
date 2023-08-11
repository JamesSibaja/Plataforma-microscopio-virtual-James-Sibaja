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


