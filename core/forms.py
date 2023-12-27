from django import forms

from django.forms import ModelForm
from core.models import *
from django.core.validators import MinLengthValidator



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
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre', label_suffix=' ')
    

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['name']
        redirect_url = 'core:services'
        
    name_attrs= {
        'max_length': 20,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre', label_suffix=' ')


class BedForm(ModelForm):
    class Meta:
        model = Bed
        fields = ['name', 'floor', 'service']
        redirect_url = 'core:beds'
        
    name_attrs= {
        'max_length': 10,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre', label_suffix=' ')
    
    floor_attrs= {
        'class': 'field',
    }
    floor = forms.IntegerField(widget=forms.NumberInput(attrs=floor_attrs), label='Planta', label_suffix=' ')

    service_attrs= {
        'class': 'field',
    }
    service = forms.ModelChoiceField(queryset= Service.objects.all(), widget=forms.Select(attrs=service_attrs), label='Servicio', label_suffix=' ')


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
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre', label_suffix=' ')    


class DrugForm(ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'NDC', 'drugType']
        redirect_url = 'core:drugs'
        
    name_attrs= {
        'max_length': 30,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre', label_suffix=' ')
    
    NDC_attrs= {
        'max_length': 7,
        'min': 0,
        'class': 'field',
    }
    NDC = forms.IntegerField(widget=forms.NumberInput(attrs=NDC_attrs), label='NDC', label_suffix=' ', required=False)
    
    drugType_attrs= {
        'class': 'field',
    }
    drugType = forms.ModelChoiceField(queryset=DrugType.objects.all(), widget=forms.Select(attrs=drugType_attrs), required=False, label='Grupo', label_suffix=' ')
    
    
class StoragedDrugForm(ModelForm):
    class Meta:
        model = StoragedDrug
        fields = ['drug', 'quantity']
        redirect_url = 'core:storagedDrugs'
        
    drug_attrs= {
        'class': 'field',
    }
    drug = forms.ModelChoiceField(queryset= Drug.objects.all(), widget=forms.Select(attrs=drug_attrs), label='Medicamento', label_suffix=' ')
    
    quantity_attrs= {
        'class': 'field',
        'min': 0,
    }
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs=quantity_attrs), label='Cantidad', label_suffix=' ')
    
    
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
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre', label_suffix=' ')
    
    
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        redirect_url = 'core:users'
        
    username_attrs= {
        'max_length': 20,
        'class': 'field',
    }
    username = forms.CharField(widget=forms.TextInput(attrs=username_attrs), label='Nombre de usuario', label_suffix=' ')

    password_attrs = {
    'max_length': 20,
    'class': 'field',
    }
    password = forms.CharField(widget=forms.PasswordInput(attrs=password_attrs), label='Contraseña', label_suffix=' ')


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'historyNumber', 'doctor', 'history', 'constants', 'bed', 'admissionDate']
        redirect_url = 'core:patients'
        
    name_attrs= {
        'max_length': 30,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre', label_suffix=' ')

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
        'class': 'field',
    }
    admissionDate = forms.DateField(widget=forms.DateInput(attrs=admissionDate_attrs), label='Fecha de ingreso', label_suffix=' ')


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
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Material', label_suffix=' ')
    
    materialType_attrs= {
        'max_length': 1,
        'class': 'field',
    }
    materialType = forms.ChoiceField(choices=materialTypes.values(), widget=forms.Select(attrs=name_attrs), label='Material', label_suffix=' ')
    

class StoragedLabMaterialForm(ModelForm):
    class Meta:
        model = StoragedLabMaterial
        fields = ['labMaterial', 'storage', 'quantity']
        redirect_url = 'core:storagedLabMaterials'
        
    labMaterial_attrs= {
        'class': 'field',
    }
    labMaterial = forms.ModelChoiceField(queryset= LabMaterial.objects.all(), widget=forms.Select(attrs=labMaterial_attrs), label='Material', label_suffix=' ')

    storage_attrs= {
        'class': 'field',
    }
    storage = forms.ModelChoiceField(queryset= Storage.objects.all(), widget=forms.Select(attrs=storage_attrs), label='Almacén', label_suffix=' ') 

    quantity_attrs= {
        'class': 'field',
        'min': 0,
    }
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs=quantity_attrs), label='Cantidad', label_suffix=' ')
    

class SampleForm(ModelForm):
    class Meta:
        model = Sample
        fields = ['sampleType', 'storage', 'patient', 'date']
        redirect_url = 'core:samples'
        
    sampleType_attrs= {
        'class': 'field',
    }
    sampleType = forms.ChoiceField(choices= sampleTypes, widget=forms.Select(attrs=sampleType_attrs), label='Tipo de muestra', label_suffix=' ')

    storage_attrs= {
        'class': 'field',
    }
    storage = forms.ModelChoiceField(queryset= Storage.objects.all(), widget=forms.Select(attrs=storage_attrs), label='Almacén', label_suffix=' ') 

    patient_attrs= {
        'class': 'field',
    }
    patient = forms.ModelChoiceField(queryset= Patient.objects.all(), widget=forms.Select(attrs=patient_attrs), label='Paciente', label_suffix=' ')
    
    date_attrs= {
        'class': 'field',
    }
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs=date_attrs), label='Fecha de muestra', label_suffix=' ')


### BLOOD ###
class BloodForm(ModelForm):
    class Meta:
        model = Blood
        fields = ['BloodGroup', 'capacity', 'date', 'tests', 'reserved']
        redirect_url = 'core:blood'
        
    BloodGroup_attrs= {
        'class': 'field',
    }
    BloodGroup = forms.ChoiceField(choices= bloodGroups, widget=forms.Select(attrs=BloodGroup_attrs), label='Grupo sanguíneo', label_suffix=' ')

    capacity_attrs= {
        'class': 'field',
    }
    capacity = forms.IntegerField(widget=forms.NumberInput(attrs=capacity_attrs), label='Volumen de sangre (mL)', label_suffix=' ')

    date_attrs= {
        'class': 'field',
    }
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs=date_attrs), label='Fecha de recepción', label_suffix=' ')

    tests_attrs= {
        'class': 'field',
    }
    tests = forms.IntegerField(widget=forms.NumberInput(attrs=tests_attrs), label='Número de pruebas', label_suffix=' ')

    reserved_attrs= {
        'class': 'field',
    }
    reserved = forms.BooleanField(widget=forms.CheckboxInput(attrs=reserved_attrs), label='Reservada', label_suffix=' ', required=False)

