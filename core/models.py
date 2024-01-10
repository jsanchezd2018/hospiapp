from datetime import timedelta
from django.db import models

### CONSTANTS ###
HISTORY_NUMBER_LENGTH = 14
NDC_LENGTH = 7

### AUXILIAR FUNCTIONS ###
def genericBooleanVerbose(bool):
    if bool:
        return 'Sí'
    else:
        return 'No'

def genericNoneVerbose(potencialNone):
    if potencialNone:
        return potencialNone
    else:
        return 'Sin asignar'


### PHYSICAL PLACES ###
class Storage(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name
    
class LabStorage(models.Model):
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
        return Patient.objects.filter(bed=self).__len__() == 1


### DRUGS ###
class DrugType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name

class Drug(models.Model):
    name = models.CharField(max_length=30, unique=True)
    NDC = models.CharField(max_length=NDC_LENGTH, unique=True, null=True, blank=True)
    drugType = models.ForeignKey(DrugType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    @property
    def verbose_NDC(self):
        return genericNoneVerbose(self.NDC)
    @property
    def verbose_drugType(self):
        return genericNoneVerbose(self.drugType)
    @property
    def total(self):
        result = 0
        for drug in StoragedDrug.objects.filter(drug=self):
            result += drug.quantity
        return result

class StoragedDrug(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    expirationDate = models.DateField(null=True, blank=True)

    class Meta:
        models.UniqueConstraint(fields=['drug', 'storage'], name='no_multiplicity')

    def __str__(self) -> str:
        return self.drug.name
    
    @property
    def verbose_storage(self):
        return genericNoneVerbose(self.storage)
    @property
    def verbose_expirationDate(self):
        return genericNoneVerbose(self.expirationDate)


### PEOPLE ###
class Doctor(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.name

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.username

class Patient(models.Model):
    name = models.CharField(max_length=30)
    historyNumber = models.CharField(max_length=HISTORY_NUMBER_LENGTH, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    history = models.CharField(max_length=500, null=True, blank=True)
    constants = models.CharField(max_length=50, null=True, blank=True)
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True)
    admissionDate = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    @property
    def verbose_historyNumber(self):
        return genericNoneVerbose(self.historyNumber)
    @property
    def verbose_doctor(self):
        return genericNoneVerbose(self.doctor)
    @property
    def verbose_constants(self):
        return genericNoneVerbose(self.constants)
    @property
    def verbose_history(self):
        return genericNoneVerbose(self.history)
    @property
    def verbose_bed(self):
        return genericNoneVerbose(self.bed)
    @property
    def verbose_admissionDate(self):
        return genericNoneVerbose(self.admissionDate)
    
    

### LAB ###

materialTypes = {
                    '1': 'Material común',
                    '2': 'Reactivos refrigerados',
                    '3': 'Reactivos en polvo',
                    '4': 'Pines reactivos',
                }

sampleTypes = {
                '1': 'Sangre',
                '2': 'Heces',
                '3': 'Orina',
                '4': 'Leche con bacterias',
                '5': 'Cultivos',
                '6': 'Otros',
            }

sampleDurations = {
                    '1': 7,
                    '2': 14,
                    '3': 7,
                    '4': 1000,
                    '5': 1000,
                    '6': 1000,
}

class LabMaterial(models.Model):
    name = models.CharField(max_length=20, unique=True)
    materialType = models.CharField(max_length=1)

    def __str__(self) -> str:
        return self.name
    
    @property
    def verbose_materialType(self):
        return materialTypes[self.materialType]
    
    @property
    def total(self):
        result = 0
        for labMaterial in StoragedLabMaterial.objects.filter(labMaterial=self):
            result += labMaterial.quantity
        return result

class StoragedLabMaterial(models.Model):
    labMaterial = models.ForeignKey(LabMaterial, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return self.labMaterial.name
    
    @property
    def verbose_storage(self):
        return genericNoneVerbose(self.storage)

    class Meta:
        models.UniqueConstraint(fields=['labMaterial', 'storage'], name='no_multiplicity')

class Sample(models.Model):
    sampleType = models.CharField(max_length=1)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    data = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return self.patient.name + '_' + self.sampleType.value + '_' + self.date
    
    @property
    def expirationDate(self):
        return self.date + timedelta(days=sampleDurations[self.sampleType])


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

processTypes = {
            '1': 'Con glóbulos',
            '2': 'Centrifugado (plaquetas)',
            '3': 'Plasma',
}

processDurations = {
                    '1': 42,
                    '2': 7,
                    '3': 1000,
}

class Blood(models.Model):
    bloodGroup = models.CharField(max_length=1)
    capacity = models.IntegerField()
    date = models.DateTimeField()
    tests = models.IntegerField()
    reserved = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    process = models.CharField(max_length=1)
    
    def __str__(self) -> str:
        return self.pk
    
    @property
    def expirationDate(self):
        return self.date + timedelta(days=processDurations[self.process])