import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VirtualMicroscope.settings')
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Slide(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=500)
    

    zoomI = models.IntegerField()
    zoomM = models.IntegerField()
    path = models.CharField(max_length=20)
    image = models.ImageField(upload_to='slides')
    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('micro-slide', args=[str(self.id)])

    def getAbsoluteUrl(self):
        return reverse('micro-slide-full', args=[str(self.id)])

