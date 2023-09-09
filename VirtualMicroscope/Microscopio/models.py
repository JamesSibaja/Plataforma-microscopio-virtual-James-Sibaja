import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VirtualMicroscope.settings')
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class OpenSlide(models.Model):
    name = models.CharField(unique=True, max_length=50)
    path = models.CharField(max_length=50,null=True)
    assembled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('open-micro-slide', args=[str(self.id)])


class Slide(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=500)
    assembled = models.BooleanField(default=False)
    rawSlide = models.ForeignKey(OpenSlide, on_delete=models.CASCADE, null=True)
    zoomI = models.IntegerField(null=True)
    zoomM = models.IntegerField(null=True)
    path = models.CharField(max_length=50,null=True)
    image = models.ImageField(upload_to='slides',null=True,)
    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('micro-slide', args=[str(self.id)])

    def getAbsoluteUrl(self):
        return reverse('micro-slide-full', args=[str(self.id)])

