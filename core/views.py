from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from core import urls


from .forms import *

@csrf_protect
@login_required
def index(request):
    return render(request, 'index.html')

### GENERIC CONSTANTS ###
N = 10

### GENERIC FUNCTIONS ###
@csrf_protect
@login_required
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
    return render(request, 'forms/genericForm.html', context=ctx)

@csrf_protect
@login_required
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
    return render(request, 'forms/genericForm.html', context=ctx)

@csrf_protect
@login_required
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
    return render(request, 'forms/genericDeletion.html', context=ctx)


### PHYSICAL PLACES ###

### STORAGES ###
@csrf_protect
@login_required
def createStorage(request):
    return createGeneric(request, StorageForm, 'core:createStorage', 'Nuevo almacén')

@csrf_protect
@login_required
def editStorage(request, pk):
    return editGeneric(request, StorageForm, pk, 'core:editStorage', 'Editar almacén')

@csrf_protect
@login_required
def deleteStorage(request, pk):
    return deleteGeneric(request, StorageForm, pk, 'core:deleteStorage', 'Borrar almacén')

@csrf_protect
@login_required
def storages(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    storages = Storage.objects.filter( name__icontains=query_generic ).order_by('name')
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
@csrf_protect
@login_required
def createService(request):
    return createGeneric(request, ServiceForm, 'core:createService', 'Nuevo servicio')

@csrf_protect
@login_required
def editService(request, pk):
    return editGeneric(request, ServiceForm, pk, 'core:editService', 'Editar servicio')

@csrf_protect
@login_required
def deleteService(request, pk):
    return deleteGeneric(request, ServiceForm, pk, 'core:deleteService', 'Borrar servicio')

@csrf_protect
@login_required
def services(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    services = Service.objects.filter( name__icontains=query_generic ).order_by('name')
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
@csrf_protect
@login_required
def createBed(request):
    return createGeneric(request, BedForm, 'core:createBed', 'Nueva cama')

@csrf_protect
@login_required
def editBed(request, pk):
    return editGeneric(request, BedForm, pk, 'core:editBed', 'Editar cama')

@csrf_protect
@login_required
def deleteBed(request, pk):
    return deleteGeneric(request, BedForm, pk, 'core:deleteBed', 'Borrar cama')

@csrf_protect
@login_required
def beds(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    query_floor = request.GET.get('query_floor', '')
    query_service = request.GET.get('query_service', '0')
    beds = Bed.objects.filter(name__icontains=query_generic).order_by('name')
    if query_floor != '':
        beds = beds.filter(floor__exact=query_floor)
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
        'services': Service.objects.all(),
        'query_generic': query_generic,
        'query_floor': query_floor,
        'query_service': int(query_service),
    }
    return render(request, 'masterViewers/beds.html', context=ctx)


### DRUGS ###

### DRUGS ###
@csrf_protect
@login_required
def createDrug(request):
    return createGeneric(request, DrugForm, 'core:createDrug', 'Nuevo medicamento')

@csrf_protect
@login_required
def editDrug(request, pk):
    return editGeneric(request, DrugForm, pk, 'core:editDrug', 'Editar medicamento')

@csrf_protect
@login_required
def deleteDrug(request, pk):
    return deleteGeneric(request, DrugForm, pk, 'core:deleteDrug', 'Borrar medicamento')

@csrf_protect
@login_required
def drugs(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    query_type = request.GET.get('query_type', '0')
    drugs = Drug.objects.filter( Q(name__icontains=query_generic) | Q(NDC__icontains=query_generic) ).order_by('name')
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
@csrf_protect
@login_required
def createDrugType(request):
    return createGeneric(request, DrugTypeForm, 'core:createDrugType', 'Nuevo grupo de medicamentos')

@csrf_protect
@login_required
def editDrugType(request, pk):
    return editGeneric(request, DrugTypeForm, pk, 'core:editDrugType', 'Editar grupo de medicamentos')

@csrf_protect
@login_required
def deleteDrugType(request, pk):
    return deleteGeneric(request, DrugTypeForm, pk, 'core:deleteDrugType', 'Borrar grupo de medicamentos')

@csrf_protect
@login_required
def drugTypes(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    drugTypes = DrugType.objects.filter( name__icontains=query_generic ).order_by('name')
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
@csrf_protect
@login_required
def createStoragedDrug(request):
    return createGeneric(request, StoragedDrugForm, 'core:createStoragedDrug', 'Nuevo uwu')

@csrf_protect
@login_required
def editStoragedDrug(request, pk):
    return editGeneric(request, StoragedDrugForm, pk, 'core:editStoragedDrug', 'Editar uwu')

@csrf_protect
@login_required
def deleteStoragedDrug(request, pk):
    return deleteGeneric(request, StoragedDrugForm, pk, 'core:deleteStoragedDrug', 'Borrar uwu')

@csrf_protect
@login_required
def storagedDrugs(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    storagedDrugs = StoragedDrug.objects.filter( name__icontains=query_generic ).order_by('drug.name')
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

@csrf_protect
@login_required
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
@csrf_protect
@login_required
def createDoctor(request):
    return createGeneric(request, DoctorForm, 'core:createDoctor', 'Nuevo médico')

@csrf_protect
@login_required
def editDoctor(request, pk):
    return editGeneric(request, DoctorForm, pk, 'core:editDoctor', 'Editar médico')

@csrf_protect
@login_required
def deleteDoctor(request, pk):
    return deleteGeneric(request, DoctorForm, pk, 'core:deleteDoctor', 'Borrar médico')

@csrf_protect
@login_required
def doctors(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    doctors = Doctor.objects.filter( Q(name__icontains=query_generic) ).order_by('name')
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
'''@csrf_protect
@login_required
def createUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:users')
    else:
        form = UserCreationForm()
    return render(request, 'forms/genericForm.html', {'form': form})'''

@csrf_protect
@login_required
def createUser(request):
    return createGeneric(request, UserForm, 'core:createUser', 'Nuevo usuario')

@csrf_protect
@login_required
def editUser(request, pk):
    return editGeneric(request, UserForm, pk, 'core:editUser', 'Editar usuario')

@csrf_protect
@login_required
def deleteUser(request, pk):
    return deleteGeneric(request, UserForm, pk, 'core:deleteUser', 'Borrar usuario')

@csrf_protect
@login_required
def users(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    users = User.objects.filter(Q(name__icontains=query_generic)).order_by('username')
    # Paginator
    paginator = Paginator(users, N)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'users': users,
        'query_generic': query_generic,
    }
    return render(request, 'masterViewers/users.html', context=ctx)

def userLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:index')
    else:
        form = AuthenticationForm()
    return render(request, 'forms/genericForm.html', {'form': form})

@csrf_protect
@login_required
def userLogout(request):
    logout(request)
    return redirect('index.html')


### PATIENTS ###
### MASTER PART ###
@csrf_protect
@login_required
def deletePatient(request, pk):
    return deleteGeneric(request, PatientForm, pk, 'core:deletePatient', 'Borrar paciente')

@csrf_protect
@login_required
def patients(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    patients = Patient.objects.filter( Q(name__icontains=query_generic) ).order_by('name')
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


### FUNCTIONALITY PART ###
@csrf_protect
@login_required
def patientsManagement(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    query_doctor = request.GET.get('query_doctor', '0')
    query_bed = request.GET.get('query_bed', '0')
    query_floor = request.GET.get('query_floor', '')
    query_service = request.GET.get('query_service', '0')
    patients = Patient.objects.filter(name__icontains=query_generic).order_by('name')
    if(query_doctor != '0'):
        patients = patients.filter(doctor__exact=query_doctor)
    if(query_bed != '0'):
        patients = patients.filter(bed__exact=query_bed)
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
        'doctors': Doctor.objects.all(),
        'backendURL': urls.backendURL,
        'query_generic': query_generic,
        'query_doctor': int(query_doctor),
        'query_bed': int(query_bed),
        'query_floor': query_floor,
        'query_service': int(query_service),
        'backendURL': urls.backendURL,
        'services': Service.objects.all(),
        'bed': Bed.objects.all(),
    }
    return render(request, 'functionalities/patientsManagement.html', context=ctx)

@csrf_protect
@login_required
def createPatient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:patientsManagement')
    else:
        form = PatientForm()
    
    ctx = {
        'form': form,
        'title': 'Ingresar paciente nuevo',
        'back_url': 'core:patientsManagement',
        'function_url': 'core:createPatient',
        'backendURL': urls.backendURL,
        'services': Service.objects.all(),
    }
    return render(request, 'forms/patientForm.html', context=ctx)

@csrf_protect
@login_required
def editPatient(request, pk):
    object = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect('core:patientsManagement')
    else:
        form = PatientForm(instance=object)
    
    ctx = {
        'form': form,
        'title': 'Ingresar paciente existente / Cambiar información del paciente',
        'back_url': 'core:patientsManagement',
        'function_url': 'core:editPatient',
        'pk': pk,
        'services': Service.objects.all()
    }
    return render(request, 'forms/patientForm.html', context=ctx)

@csrf_protect
@login_required
def dischargePatient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.admissionDate = None
    patient.bed = None
    patient.save()
    return redirect('core:patientsManagement')
    

### BACKEND FUNCTIONS ###
@csrf_protect
@csrf_protect
@login_required
def filter(request, pk_service, floor):
    if request.method == 'GET':
        beds = Bed.objects.all()
        if(pk_service != 0): beds = beds.filter(service__exact=pk_service)
        if(floor != 0): beds = beds.filter(floor__exact=floor)
        result = []
        for bed in beds:
            if not bed.ocupied:
                result.append({'key': bed.pk, 'value': bed.name})
        return JsonResponse({'result': result})
    else:
        return JsonResponse({})
    

@csrf_protect
@csrf_protect
@login_required
def filterInManagement(request, pk_service, floor):
    if request.method == 'GET':
        beds = Bed.objects.all()
        if(pk_service != 0): beds = beds.filter(service__exact=pk_service)
        if(floor != 0): beds = beds.filter(floor__exact=floor)
        result = []
        for bed in beds:
            result.append({'key': bed.pk, 'value': bed.name})
        return JsonResponse({'result': result})
    else:
        return JsonResponse({})
    

@csrf_protect
@csrf_protect
@login_required
def viewPatient(request, pk):
    if request.method == 'GET':

        patient = get_object_or_404(Patient, pk=pk)
        if patient.doctor:
            patient_doctor = patient.doctor.name
        else:
            patient_doctor = 'Sin asignar'
        
        if patient.bed:
            bed = get_object_or_404(Bed, pk=patient.bed.pk)
            bed_name = bed.name
            bed_floor = bed.floor
            bed_service = bed.service.name
        else:
            bed_name = 'Sin asignar'
            bed_floor = 'Sin asignar'
            bed_service = 'Sin asignar'
        
        return JsonResponse({
                                'backendPatient_name': patient.name,
                                'backendPatient_historyNumber': str(patient.verbose_historyNumber).zfill(HISTORY_NUMBER_LENGTH),
                                'backendPatient_doctor': patient_doctor,
                                'backendPatient_constants': patient.verbose_constants,
                                'backendPatient_admissionDate': patient.verbose_admissionDate,
                                'backendPatient_history': patient.verbose_history,
                                'backendBed_name': bed_name,
                                'backendBed_floor': bed_floor,
                                'backendBed_service': bed_service,
                            })
    else:
        return JsonResponse({})