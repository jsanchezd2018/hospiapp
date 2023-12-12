from django.db import models

### PHYSICAL PLACES ###
class Storage(models.Model):
    name = models.CharField(max_length=20, unique=True)

class Service(models.Model):
    name = models.CharField(max_length=20, unique=True)

class Bed(models.Model):
    name = models.CharField(max_length=10, unique=True)
    floor = models.IntegerField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    @property
    def ocupied(self):
        return Patient.objects.filter(bed=self.pk).acount() > 0


### DRUGS ###
class DrugType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name

class Drug(models.Model):
    name = models.CharField(max_length=30, unique=True)
    NDC = models.IntegerField(unique=True, null=True, blank=True)
    drugType = models.ForeignKey(DrugType, on_delete=models.SET_NULL, null=True, blank=True)

class StoragedDrug(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()

    class Meta:
        models.UniqueConstraint(fields=['drug', 'storage'], name='no_multiplicity')


### PEOPLE ###
class Doctor(models.Model):
    name = models.CharField(max_length=30, unique=True)
    active = models.BooleanField(default=True)

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=15)

class Patient(models.Model):
    historyNumer = models.IntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=30)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, null=True, blank=True)
    history = models.CharField(max_length=500, null=True, blank=True)
    constants = models.CharField(max_length=50, null=True, blank=True)
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

