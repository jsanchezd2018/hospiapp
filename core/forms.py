from django import forms
from django.forms import ModelForm
from core.models import *
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


### PHYSICAL PLACES ###
class StorageForm(ModelForm):
    class Meta:
        model = Storage
        fields = ['name']
        redirect_url = 'core:storages'
        
    name_attrs= {
        'max_length': 20,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre (*)', label_suffix=' ')


class LabStorageForm(ModelForm):
    class Meta:
        model = LabStorage
        fields = ['name']
        redirect_url = 'core:labStorages'
        
    name_attrs= {
        'max_length': 20,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre (*)', label_suffix=' ')    
    

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['name']
        redirect_url = 'core:services'
        
    name_attrs= {
        'max_length': 20,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre (*)', label_suffix=' ')


class BedForm(ModelForm):
    class Meta:
        model = Bed
        fields = ['name', 'floor', 'service']
        redirect_url = 'core:beds'
        
    name_attrs= {
        'max_length': 10,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre (*)', label_suffix=' ')
    
    floor_attrs= {
        'class': 'field',
    }
    floor = forms.IntegerField(widget=forms.NumberInput(attrs=floor_attrs), label='Planta (*)', label_suffix=' ')

    service_attrs= {
        'class': 'field',
    }
    service = forms.ModelChoiceField(queryset= Service.objects.all(), widget=forms.Select(attrs=service_attrs), label='Servicio (*)', label_suffix=' ')


### DRUGS ###
class DrugTypeForm(ModelForm):
    class Meta:
        model = DrugType
        fields = ['name']
        redirect_url = 'core:drugTypes'
        
    name_attrs= {
        'max_length': 30,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre (*)', label_suffix=' ')    


class DrugForm(ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'NDC', 'drugType']
        redirect_url = 'core:drugs'
        
    name_attrs= {
        'max_length': 30,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre (*)', label_suffix=' ')
    
    NDC_attrs= {
        'max_length': NDC_LENGTH,
        'class': 'field',
    }
    NDC = forms.CharField(widget=forms.TextInput(attrs=NDC_attrs), label='NDC', label_suffix=' ', required=False, validators=[MinLengthValidator(NDC_LENGTH)])
    
    drugType_attrs= {
        'class': 'field',
    }
    drugType = forms.ModelChoiceField(queryset=DrugType.objects.all(), widget=forms.Select(attrs=drugType_attrs), required=False, label='Grupo', label_suffix=' ')
    
    
class StoragedDrugForm(ModelForm):
    class Meta:
        model = StoragedDrug
        fields = ['drug', 'quantity', 'expirationDate', 'storage']
        redirect_url = 'core:storagedDrugs'
        
    drug_attrs= {
        'class': 'field',
        'id': 'drug_selector'
    }
    drug = forms.ModelChoiceField(queryset= Drug.objects.all(), widget=forms.Select(attrs=drug_attrs), label='Medicamento (*)', label_suffix=' ')
    
    quantity_attrs= {
        'class': 'field',
        'min': 1,
    }
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs=quantity_attrs), label='Cantidad (*)', label_suffix=' ')

    expirationDate_attrs= {
        'class': 'field date',
    }
    expirationDate = forms.DateField(widget=forms.DateInput(attrs=expirationDate_attrs), label='Fecha de caducidad', label_suffix=' ', required=False)

    storage_attrs= {
        'class': 'field date',
    }
    storage = forms.ModelChoiceField(queryset=Storage.objects.all(), widget=forms.Select(attrs=storage_attrs), label='Almacén', label_suffix=' ')


# diferent form for creation and edition
class StoragedDrugFormEdition(ModelForm):
    class Meta:
        model = StoragedDrug
        fields = ['quantity', 'expirationDate', 'storage']
        redirect_url = 'core:storagedDrugs'
    
    quantity_attrs= {
        'class': 'field',
        'min': 0,
    }
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs=quantity_attrs), label='Cantidad (*)', label_suffix=' ')

    expirationDate_attrs= {
        'class': 'field',
    }
    expirationDate = forms.DateField(widget=forms.DateInput(attrs=expirationDate_attrs), label='Fecha de caducidad', label_suffix=' ', required=False)

    storage_attrs= {
        'class': 'field',
    }
    storage = forms.ModelChoiceField(queryset=Storage.objects.all(), widget=forms.Select(attrs=storage_attrs), label='Almacén (*)', label_suffix=' ')
    
    
### PEOPLE ###
class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['name']
        redirect_url = 'core:doctors'
        
    name_attrs= {
        'max_length': 30,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre (*)', label_suffix=' ')
    
    
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        redirect_url = 'core:users'
        
    username_attrs= {
        'max_length': 20,
        'class': 'field',
    }
    username = forms.CharField(widget=forms.TextInput(attrs=username_attrs), label='Nombre de usuario (*)', label_suffix=' ')

    password_attrs = {
    'max_length': 20,
    'class': 'field',
    }
    password = forms.CharField(widget=forms.PasswordInput(attrs=password_attrs), label='Contraseña (*)', label_suffix=' ')

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'historyNumber', 'doctor', 'history', 'constants', 'bed', 'admissionDate']
        redirect_url = 'core:patients'
        
    name_attrs= {
        'max_length': 30,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre (*)', label_suffix=' ')

    historyNumber_attrs = {
        'max_length': HISTORY_NUMBER_LENGTH,
        'class': 'field',
    }
    historyNumber = forms.CharField(widget=forms.TextInput(attrs=historyNumber_attrs), label='Número de Historia', label_suffix=' ', required=False, validators=[MinLengthValidator(HISTORY_NUMBER_LENGTH)])

    doctor_attrs = {
        'class': 'field',
    }
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), widget=forms.Select(attrs=doctor_attrs), label='Doctor', label_suffix=' ', required=False)

    history_attrs = {
        'max_length': 500,
        'class': 'field',
    }
    history = forms.CharField(widget=forms.Textarea(attrs=history_attrs), label='Historia', label_suffix=' ', required=False)

    constants_attrs = {
        'max_length': 50,
        'class': 'field',
    }
    constants = forms.CharField(widget=forms.TextInput(attrs=constants_attrs), label='Constantes', label_suffix=' ', required=False)

    bed_attrs = {
        'class': 'field',
        'id': 'bed_selector'
    }
    bed = forms.ModelChoiceField(queryset=Bed.objects.all(), widget=forms.Select(attrs=bed_attrs), label='Cama', label_suffix=' ', required=False)

    admissionDate_attrs = {
        'class': 'field date',
    }
    admissionDate = forms.DateField(widget=forms.DateInput(attrs=admissionDate_attrs), label='Fecha de ingreso (*)', label_suffix=' ')


### LAB ###
class LabMaterialForm(ModelForm):
    class Meta:
        model = LabMaterial
        fields = ['name', 'materialType']
        redirect_url = 'core:labMaterials'
        
    name_attrs= {
        'max_length': 30,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Material (*)', label_suffix=' ')
    
    materialType_attrs= {
        'max_length': 1,
        'class': 'field',
    }
    materialType = forms.ChoiceField(choices=materialTypes.items(), widget=forms.Select(attrs=name_attrs), label='Tipo de material (*)', label_suffix=' ')
    

class StoragedLabMaterialForm(ModelForm):
    class Meta:
        model = StoragedLabMaterial
        fields = ['labMaterial', 'quantity', 'storage']
        redirect_url = 'core:storagedLabMaterials'
        
    labMaterial_attrs= {
        'class': 'field',
        'id': 'labMaterial_selector',
    }
    labMaterial = forms.ModelChoiceField(queryset= LabMaterial.objects.all(), widget=forms.Select(attrs=labMaterial_attrs), label='Material (*)', label_suffix=' ')

    quantity_attrs= {
        'class': 'field',
        'min': 0,
    }
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs=quantity_attrs), label='Cantidad (*)', label_suffix=' ')

    storage_attrs= {
        'class': 'field',
        'min': 0,
    }
    storage = forms.ModelChoiceField(queryset=LabStorage.objects.all(), widget=forms.Select(attrs=storage_attrs), label='Almacén (*)', label_suffix=' ')


# diferent form for creation and edition
class StoragedLabMaterialFormEdition(ModelForm):
    class Meta:
        model = StoragedLabMaterial
        fields = ['quantity', 'storage']
        redirect_url = 'core:storagedLabMaterials'
        
    quantity_attrs= {
        'class': 'field',
        'min': 0,
    }
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs=quantity_attrs), label='Cantidad (*)', label_suffix=' ')

    storage_attrs= {
        'class': 'field',
    }
    storage = forms.ModelChoiceField(queryset=LabStorage.objects.all(), widget=forms.Select(attrs=storage_attrs), label='Almacén (*)', label_suffix=' ')
    

class SampleForm(ModelForm):
    class Meta:
        model = Sample
        fields = ['sampleType', 'patient', 'date', 'data', 'storage']
        redirect_url = 'core:samples'
        
    sampleType_attrs= {
        'class': 'field',
    }
    sampleType = forms.ChoiceField(choices= sampleTypes.items(), widget=forms.Select(attrs=sampleType_attrs), label='Tipo de muestra (*)', label_suffix=' ')

    patient_attrs= {
        'class': 'field',
        'id': 'patient_selector'
    }
    patient = forms.ModelChoiceField(queryset= Patient.objects.all(), widget=forms.Select(attrs=patient_attrs), label='Paciente (*)', label_suffix=' ')
    
    date_attrs= {
        'class': 'field datetime',
    }
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs=date_attrs), label='Fecha de muestra (*)', label_suffix=' ')

    data_attrs= {
        'class': 'field',
    }
    data = forms.CharField(widget=forms.Textarea(attrs=data_attrs), label='Observaciones y resultados', label_suffix=' ', required= False)

    storage_attrs = {
        'class': 'field',
    }
    storage = forms.ModelChoiceField(queryset=LabStorage.objects.all(), widget=forms.Select(attrs=storage_attrs), label='Almacén', label_suffix=' ')


# diferent form for creation and edition
class SampleFormEdition(ModelForm):
    class Meta:
        model = Sample
        fields = ['data', 'storage']
        redirect_url = 'core:samples'
        
    data_attrs= {
        'class': 'field',
    }
    data = forms.CharField(widget=forms.Textarea(attrs=data_attrs), label='Observaciones y resultados (*)', label_suffix=' ', required= False)

    storage_attrs= {
        'class': 'field',
    }
    storage = forms.ModelChoiceField(queryset=LabStorage.objects.all(), widget=forms.Select(attrs=storage_attrs), label='Almacén (*)', label_suffix=' ')


class BloodForm(ModelForm):
    class Meta:
        model = Blood
        fields = ['bloodGroup', 'capacity', 'date', 'tests', 'reserved', 'process', 'storage']
        redirect_url = 'core:blood'
        
    bloodGroup_attrs= {
        'class': 'field',
    }
    bloodGroup = forms.ChoiceField(choices= bloodGroups.items(), widget=forms.Select(attrs=bloodGroup_attrs), label='Grupo sanguíneo (*)', label_suffix=' ')

    capacity_attrs= {
        'class': 'field',
    }
    capacity = forms.IntegerField(widget=forms.NumberInput(attrs=capacity_attrs), label='Volumen de sangre (mL) (*)', label_suffix=' ')

    date_attrs= {
        'class': 'field datetime',
    }
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs=date_attrs), label='Fecha de recepción (*)', label_suffix=' ')

    tests_attrs= {
        'class': 'field',
        'min_value': 0,
    }
    tests = forms.IntegerField(widget=forms.NumberInput(attrs=tests_attrs), label='Número de pruebas (*)', label_suffix=' ', initial=0)

    reserved_attrs= {
        'class': 'field',
    }
    reserved = forms.ModelChoiceField(queryset=Patient.objects.all(), widget=forms.Select(attrs=reserved_attrs), label='Reserva',
                                      label_suffix=' ', required=False)

    process_attrs= {
        'class': 'field',
    }
    process = forms.ChoiceField(choices=processTypes.items(), widget=forms.Select(attrs=process_attrs), label='Tipo (*)', label_suffix=' ')

    storage_attrs= {
        'class': 'field',
    }
    storage = forms.ModelChoiceField(queryset=LabStorage.objects.all(), widget=forms.Select(attrs=storage_attrs), label='Almacén (*)', label_suffix=' ')


# diferent form for creation and edition
class BloodFormEdition(ModelForm):
    class Meta:
        model = Blood
        fields = ['tests', 'reserved', 'storage']
        redirect_url = 'core:blood'
        
    tests_attrs= {
        'class': 'field',
        'min_value': 0,
    }
    tests = forms.IntegerField(widget=forms.NumberInput(attrs=tests_attrs), label='Número de pruebas (*)', label_suffix=' ', initial=0)

    reserved_attrs= {
        'class': 'field',
    }
    reserved = forms.ModelChoiceField(queryset=Patient.objects.all(), widget=forms.Select(attrs=reserved_attrs), label='Reserva',
                                      label_suffix=' ', required=False)

    storage_attrs= {
        'class': 'field',
    }
    storage = forms.ModelChoiceField(queryset=LabStorage.objects.all(), widget=forms.Select(attrs=storage_attrs), label='Almacén',
                                      label_suffix=' ', required=False)

