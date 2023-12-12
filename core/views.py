import os
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

from hospiapp.settings import BASE_DIR
from .forms import *
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')




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


'''def deleteDrug(request, pk):
    drug = get_object_or_404(Drug, pk=pk)
    if request.method == 'POST':
        drug.delete()
        return redirect('core:drugs')

    ctx = {
        'drug': drug,
    }
    return render(request, 'genericDeletion.html', context=ctx)'''

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
    paginator = Paginator(drugs, 10)
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
    return render(request, 'drugs.html', context=ctx)




### DRUG TYPES###
'''def createDrug(request):
    if request.method == "POST":
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = DrugForm()
    
    ctx = {
        'form': form,
    }
    return render(request, 'home.html', context=ctx)'''

