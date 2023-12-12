from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

from .forms import *


def index(request):
    return render(request, 'index.html')

### GENERIC CONSTANTS ###
N = 10

### GENERIC FUNCTIONS ###
def createGeneric(request, klass, function_url, title):
    if request.method == 'POST':
        form = klass(request.POST)
        if form.is_valid():
            form.save()
            return redirect(klass.Meta.redirect_url)
    else:
        form = klass()
    
    ctx = {
        'form': form,
        'title': title,
        'back_url': klass.Meta.redirect_url,
        'function_url': function_url
    }
    return render(request, 'genericForm.html', context=ctx)

def editGeneric(request, klass, pk, function_url, title):
    object = get_object_or_404(klass.Meta.model, pk=pk)
    if request.method == 'POST':
        form = klass(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect(klass.Meta.redirect_url)
    else:
        form = klass(instance=object)
    
    ctx = {
        'form': form,
        'title': title,
        'back_url': klass.Meta.redirect_url,
        'function_url': function_url,
        'pk': pk,
    }
    return render(request, 'genericForm.html', context=ctx)

def deleteGeneric(request, klass, pk, function_url, title):
    object = get_object_or_404(klass.Meta.model, pk=pk)
    if request.method == 'POST':
        object.delete()
        return redirect(klass.Meta.redirect_url)

    ctx = {
        'object': object,
        'title': title,
        'back_url': klass.Meta.redirect_url,
        'function_url': function_url,
        'pk': pk,
    }
    return render(request, 'genericDeletion.html', context=ctx)


### DRUGS ###
def createDrug(request):
    return createGeneric(request, DrugForm, 'core:createDrug', 'Nuevo medicamento')

def editDrug(request, pk):
    return editGeneric(request, DrugForm, pk, 'core:editDrug', 'Editar medicamento')

def deleteDrug(request, pk):
    return deleteGeneric(request, DrugForm, pk, 'core:deleteDrug', 'Borrar medicamento')

def drugs(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    query_type = request.GET.get('query_type', '0')
    drugs = Drug.objects.filter( Q(name__icontains=query_generic) | Q(NDC__icontains=query_generic) )
    if query_type != '0':
        drugs = Drug.objects.filter( drugType__exact=query_type )
    # Paginator
    paginator = Paginator(drugs, N)
    page = request.GET.get('page', 1)
    try:
        drugs = paginator.page(page)
    except EmptyPage:
        drugs = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'drugs': drugs,
        'query_generic': query_generic,
        'query_type': int(query_type),
        'types': DrugType.objects.all()
    }
    return render(request, 'masterViewers/drugs.html', context=ctx)


### DRUG TYPES###
def createDrugType(request):
    return createGeneric(request, DrugTypeForm, 'core:createDrugType', 'Nuevo grupo de medicamentos')

def editDrugType(request, pk):
    return editGeneric(request, DrugTypeForm, pk, 'core:editDrugType', 'Editar grupo de medicamentos')

def deleteDrugType(request, pk):
    return deleteGeneric(request, DrugTypeForm, pk, 'core:deleteDrugType', 'Borrar grupo de medicamentos')

def drugTypes(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    drugTypes = DrugType.objects.filter( name__icontains=query_generic )
    # Paginator
    paginator = Paginator(drugTypes, N)
    page = request.GET.get('page', 1)
    try:
        drugTypes = paginator.page(page)
    except EmptyPage:
        drugTypes = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'drugTypes': drugTypes,
        'query_generic': query_generic,
    }
    return render(request, 'masterViewers/drugTypes.html', context=ctx)