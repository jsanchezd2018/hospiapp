from django.db import models

# Create your models here.

class DrugType(models.Model):
    name = models.CharField(max_length=20)

class Drug(models.Model):
    name = models.CharField(max_length=30)
    NDC = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField()
    #group = models.ForeignKey(DrugType, on_delete=models.CASCADE, null=True, blank=True)