from django.db import models
from Microscopio.models import Slide
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from jsonfield import JSONField

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=500)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sharedUsers = models.ManyToManyField(User, related_name='sharedUsers')
    invitedUsers = models.ManyToManyField(User, related_name='invitedUsers')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id),str(0),str(0)])

class ProjectSlide(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=500)


    slide = models.ForeignKey(Slide, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-slide-detail', args=[str(self.id)])
    

class Notes(models.Model):
    name = models.CharField(max_length=50)
    
    description = models.TextField(max_length=500)
    geojson_data = models.TextField(null=True, blank=True)
    show = models.BooleanField()

    xUnoPos = models.FloatField()
    yUnoPos = models.FloatField()
    xDosPos = models.FloatField()
    yDosPos = models.FloatField()
    
    project = models.ForeignKey(ProjectSlide, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name  

    def get_absolute_url(self):
        return reverse('note-detail', args=[str(self.id),str(self.project.id)])
    
