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


### PHYSICAL PLACES ###

### STORAGES ###
def createStorage(request):
    return createGeneric(request, StorageForm, 'core:createStorage', 'Nuevo almacén')

def editStorage(request, pk):
    return editGeneric(request, StorageForm, pk, 'core:editStorage', 'Editar almacén')

def deleteStorage(request, pk):
    return deleteGeneric(request, StorageForm, pk, 'core:deleteStorage', 'Borrar almacén')

def storages(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    storages = Storage.objects.filter( name__icontains=query_generic )
    # Paginator
    paginator = Paginator(storages, N)
    page = request.GET.get('page', 1)
    try:
        storages = paginator.page(page)
    except EmptyPage:
        storages = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'storages': storages,
        'query_generic': query_generic,
    }
    return render(request, 'masterViewers/storages.html', context=ctx)


### SERVICES ###
def createService(request):
    return createGeneric(request, ServiceForm, 'core:createService', 'Nuevo servicio')

def editService(request, pk):
    return editGeneric(request, ServiceForm, pk, 'core:editService', 'Editar servicio')

def deleteService(request, pk):
    return deleteGeneric(request, ServiceForm, pk, 'core:deleteService', 'Borrar servicio')

def services(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    services = Service.objects.filter( name__icontains=query_generic )
    # Paginator
    paginator = Paginator(services, N)
    page = request.GET.get('page', 1)
    try:
        services = paginator.page(page)
    except EmptyPage:
        services = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'services': services,
        'query_generic': query_generic,
    }
    return render(request, 'masterViewers/services.html', context=ctx)


### BEDS ###
def createBed(request):
    return createGeneric(request, BedForm, 'core:createBed', 'Nueva cama')

def editBed(request, pk):
    return editGeneric(request, BedForm, pk, 'core:editBed', 'Editar cama')

def deleteBed(request, pk):
    return deleteGeneric(request, BedForm, pk, 'core:deleteBed', 'Borrar cama')

def beds(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    query_floor = request.GET.get('query_generic', '0')
    query_service = request.GET.get('query_generic', '0')
    beds = Bed.objects.filter( Q(name__icontains=query_generic) | Q(floor__exact=query_floor) )
    if query_service != '0':
        beds = beds.filter( service__exact=query_service )
    # Paginator
    paginator = Paginator(beds, N)
    page = request.GET.get('page', 1)
    try:
        beds = paginator.page(page)
    except EmptyPage:
        beds = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'beds': beds,
        'query_generic': query_generic,
        'query_floor': query_floor,
        'query_service': query_service,
    }
    return render(request, 'masterViewers/beds.html', context=ctx)


### DRUGS ###

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
        drugs = drugs.filter( drugType__exact=query_type )
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


### DRUG TYPES ###
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


### STORAGED DRUGS ###   
#TODO: Esto es más de funcionalidades, primero, debo implementar el manejo de maestros,
#las backups, que es muy rápido y me ahorra tiempo y ya luego esto.
def createStoragedDrug(request):
    return createGeneric(request, StoragedDrugForm, 'core:createStoragedDrug', 'Nuevo uwu')

def editStoragedDrug(request, pk):
    return editGeneric(request, StoragedDrugForm, pk, 'core:editStoragedDrug', 'Editar uwu')

def deleteStoragedDrug(request, pk):
    return deleteGeneric(request, StoragedDrugForm, pk, 'core:deleteStoragedDrug', 'Borrar uwu')

def storagedDrugs(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    storagedDrugs = StoragedDrug.objects.filter( name__icontains=query_generic )
    # Paginator
    paginator = Paginator(storagedDrugs, N)
    page = request.GET.get('page', 1)
    try:
        storagedDrugs = paginator.page(page)
    except EmptyPage:
        storagedDrugs = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'storagedDrugs': storagedDrugs,
        'query_generic': query_generic,
    }
    return render(request, 'masterViewers/storagedDrugs.html', context=ctx)

def consumeStoragedDrug(request):
    '''# Queries
    query_generic = request.GET.get('query_generic', '')
    storagedDrugs = StoragedDrug.objects.filter( name__icontains=query_generic )
    # Paginator
    paginator = Paginator(storagedDrugs, N)
    page = request.GET.get('page', 1)
    try:
        storagedDrugs = paginator.page(page)
    except EmptyPage:
        storagedDrugs = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'storagedDrugs': storagedDrugs,
        'query_generic': query_generic,
    }
    return render(request, 'masterViewers/storagedDrugs.html', context=ctx)'''


### PEOPLE ###

### DOCTORS ###
def createDoctor(request):
    return createGeneric(request, DoctorForm, 'core:createDoctor', 'Nuevo médico')

def editDoctor(request, pk):
    return editGeneric(request, DoctorForm, pk, 'core:editDoctor', 'Editar médico')

def deleteDoctor(request, pk):
    return deleteGeneric(request, DoctorForm, pk, 'core:deleteDoctor', 'Borrar médico')

def doctors(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    doctors = Doctor.objects.filter( Q(name__icontains=query_generic) )
    # Paginator
    paginator = Paginator(doctors, N)
    page = request.GET.get('page', 1)
    try:
        doctors = paginator.page(page)
    except EmptyPage:
        doctors = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'doctors': doctors,
        'query_generic': query_generic,
    }
    return render(request, 'masterViewers/doctors.html', context=ctx)

### USERS ###
#TODO

### PATIENTS ###
def createPatient(request):
    return createGeneric(request, PatientForm, 'core:createPatient', 'Nuevo paciente')

def editPatient(request, pk):
    return editGeneric(request, PatientForm, pk, 'core:editPatient', 'Editar paciente')

def deletePatient(request, pk):
    return deleteGeneric(request, PatientForm, pk, 'core:deletePatient', 'Borrar paciente')

def patients(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    patients = Patient.objects.filter( Q(name__icontains=query_generic) )
    # Paginator
    paginator = Paginator(patients, N)
    page = request.GET.get('page', 1)
    try:
        patients = paginator.page(page)
    except EmptyPage:
        patients = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'patients': patients,
        'query_generic': query_generic,
    }
    return render(request, 'masterViewers/patients.html', context=ctx)
