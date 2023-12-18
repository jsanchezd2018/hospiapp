from django.db import models

def genericBooleanVerbose(bool):
    if bool:
        return 'Sí'
    else:
        return 'No'



### PHYSICAL PLACES ###
class Storage(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name

class Bed(models.Model):
    name = models.CharField(max_length=10, unique=True)
    floor = models.IntegerField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    @property
    def ocupied(self):
        return Patient.objects.filter(bed=self.pk).acount() == 1


### DRUGS ###
class DrugType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name

class Drug(models.Model):
    name = models.CharField(max_length=30, unique=True)
    NDC = models.IntegerField(unique=True, null=True, blank=True)
    drugType = models.ForeignKey(DrugType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class StoragedDrug(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()

    class Meta:
        models.UniqueConstraint(fields=['drug', 'storage'], name='no_multiplicity')

    def __str__(self) -> str:
        return self.drug.name


### PEOPLE ###
class Doctor(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.name

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.username

class Patient(models.Model):
    name = models.CharField(max_length=30)
    historyNumer = models.IntegerField(unique=True, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    history = models.CharField(max_length=500, null=True, blank=True)
    constants = models.CharField(max_length=50, null=True, blank=True)
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True)
    admitted = models.BooleanField(default=True)
    admissionDate = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    @property
    def verbose_admitted(self):
        return genericBooleanVerbose(self.admitted)
    

### LAB ###

materialTypes = {
                    '1': 'Reactivos refrigerados',
                    '2': 'Reactivos en polvo',
                    '3': 'Pines reactivos',
                    '4': 'Material común'
                }

sampleTypes = {
                '1': 'Sangre',
                '2': 'Heces',
                '3': 'Orina',
                '4': 'Leche con bacterias',
                '5': 'Cultivos',
                '6': 'Otros',
            }

class LabMaterial(models.Model):
    name = models.CharField(max_length=20, unique=True)
    materialType = models.CharField(max_length=1)

class StoragedLabMaterial(models.Model):
    labMaterial = models.ForeignKey(LabMaterial, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        models.UniqueConstraint(fields=['labMaterial', 'storage'], name='no_multiplicity')

class Sample(models.Model):
    sampleType = models.CharField(max_length=1)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()


### BLOOD ###

bloodGroups = {
                '1': 'A+',
                '2': 'A-',
                '3': 'B+',
                '4': 'B-',
                '5': 'AB+',
                '6': 'AB-',
                '7': '0+',
                '8': '0-', 
            }

class Blood(models.Model):
    bloodGroup = models.CharField(max_length=1)
    capacity = models.IntegerField() #mililiters
    date = models.DateTimeField()
    tests = models.IntegerField()
    reserved = models.BooleanField(default=False)
    