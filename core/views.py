import os
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage

from hospiapp.settings import BASE_DIR
from .forms import *
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')




### GENERIC FUNCTIONS ###
def createGeneric(request, klass):
    if request.method == 'POST':
        form = klass(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = klass()
    
    ctx = {
        'form': form,
    }
    return render(request, 'genericForm.html', context=ctx)

### DRUGS ###
def createDrug(request):
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = DrugForm()
    
    ctx = {
        'form': form,
    }
    return render(request, 'genericForm.html', context=ctx)

def editDrug(request, pk):
    drug = get_object_or_404(Drug, pk=pk)
    if request.method == 'POST':
        form = DrugForm(request.POST, instance=drug)
        if form.is_valid():
            form.save()
    else:
        form = DrugForm(instance=drug)
    
    ctx = {
        'form': form,
    }
    return render(request, 'genericForm.html', context=ctx)


def deleteDrug(request, pk):
    drug = get_object_or_404(Drug, pk=pk)
    if request.method == 'POST':
        drug.delete()
        return redirect('core:drugs')

    ctx = {
        'drug': drug,
    }
    return render(request, 'genericDeletion.html', context=ctx)


def drugs(request):
    drugs = Drug.objects.all()

    n = 10
    paginator = Paginator(drugs, n)

    page = request.GET.get('page', 1)

    try:
        drugs = paginator.page(page)
    except EmptyPage:
        drugs = paginator.page(paginator.num_pages)

    ctx = {
        'drugs': drugs,
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

