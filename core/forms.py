from django import forms

from django.forms import ModelForm
from core.models import *


class DrugForm(ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'NDC', 'quantity']
        
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
    
    quantity_attrs= {
        'min': 0,
        'class': 'field',
        'default': 0,
    }
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs=quantity_attrs), label='Cantidad', label_suffix=' ')
    
    '''group_attrs= {
        'class': 'field',
    }
    group = forms.ModelChoiceField(queryset=DrugType.objects.all(), widget=forms.Select(attrs=group_attrs), label='Grupo', label_suffix=' ')'''
    
    
class DrugTypeForm(ModelForm):
    class Meta:
        model = Drug
        fields = ['name']
        
    name_attrs= {
        'max_length': 30,
        'class': 'field',
    }
    name = forms.CharField(widget=forms.TextInput(attrs=name_attrs), label='Nombre', label_suffix=' ')
    

