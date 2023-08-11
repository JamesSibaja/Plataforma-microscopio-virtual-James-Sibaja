from django.urls import path, re_path
from django.conf.urls import url , include
from django.conf import settings
from django.conf.urls.static import static
from Microscopio.views import catalogo, micro, microfull

urlpatterns = [
    path('catalogo/', catalogo, name = "Catalogo"),
    path('micro/<pk>/',micro.as_view(),name='micro-slide'),
    path('microfull/<pk>/',microfull.as_view(),name='micro-slide-full')
]
