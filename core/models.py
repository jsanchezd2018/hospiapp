from django.db import models

# Create your models here.

class DrugType(models.Model):
    name = models.CharField(max_length=20)

class Drug(models.Model):
    name = models.CharField(max_length=30)
    NDC = models.IntegerField(null=True, blank=True)
    #group = models.ForeignKey(DrugType, on_delete=models.CASCADE, null=True, blank=True)

class Storage(models.Model):
    name = models.CharField(max_length=20)

class StoragedDrugs(models.Model):
    #drug = FK
    #storage = FK
    quantity = models.IntegerField()

    
