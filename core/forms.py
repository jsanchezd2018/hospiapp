from django import forms

from django.forms import ModelForm
from core.models import *


### PHYSICAL PLACES ###


### DRUGS ###
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
    

