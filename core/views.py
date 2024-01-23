# JSON
from django.http import JsonResponse
# Funciones basicas
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
# Utilidades paginas
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
# Otros archivos
from core import urls
from .forms import *
# Copias de seguridad
import os, subprocess, platform
from hospiapp.settings import BASE_DIR
from datetime import datetime


### BASICS ###
@csrf_protect
@login_required
def index(request):
    return render(request, 'index.html')


### BACKUPS ###
@csrf_protect
@login_required
def backups(request):
    try:
        date = showDate(os.path.basename(os.listdir(os.path.join(BASE_DIR, 'static\\backups'))[0])[7:17])
    except:
        date = 'Ninguna'
    return render(request, 'backups/backups.html', context={'date': date})

@csrf_protect
@login_required
def createBackup(request):
    # configuration
    user =     ''
    password = ''
    database = ''
    location = ''
    date = datetime.now()
    
    with open(os.path.join(BASE_DIR, 'static\\config\\database_config.txt')) as config_file:
        lines = config_file.readlines()
        user =     lines[0].replace('\n', '')
        password = lines[1].replace('\n', '')
        database = lines[2].replace('\n', '')
        location = lines[3].replace('\n', '')
        sql_dump = lines[4].replace('\n', '')
    file_name = os.path.join(location, 'backup_'+ str(date.year).zfill(4) + '-' + str(date.month).zfill(2) + '-' + str(date.day).zfill(2) + '.sql')

    # sqldump (depends of OS)
    if platform.system() == 'Windows': # Windows: Goes to directory and executes command
        wd = os.getcwd()
        os.chdir(sql_dump)
        subprocess.Popen(f'mysqldump -u{user} -p{password} --databases {database} > {file_name}', shell=True).wait()
        os.chdir(wd)
    elif platform.system() == 'Linux': # Linux (not Mac): Uses commnand, then moves the file
        subprocess.Popen(f'mysqldump -u{user} -p{password} --databases {database} > {file_name}', shell=True).wait()
        subprocess.Popen(f'mv {file_name}.sql {location}', shell=True).wait()
    else: # No others supported by now
        print('Es un sistema operativo no compatible con este software')

    # remove other files
    for file in os.listdir(location):
        if os.path.join(location, file) != file_name: os.remove(os.path.join(location, file))

    # Page
    return render(request, 'backups/finishedProcess.html', context={'message': 'Se ha creado la copia de seguridad'})


@csrf_protect
@login_required
def restoreBackup(request):
    # configuration
    user =     ''
    password = ''
    database = ''
    location = ''
    
    with open(os.path.join(BASE_DIR, 'static\\config\\database_config.txt')) as config_file:
        lines = config_file.readlines()
        user =     lines[0].replace('\n', '')
        password = lines[1].replace('\n', '')
        database = lines[2].replace('\n', '')
        location = lines[3].replace('\n', '')
        sql_dump = lines[4].replace('\n', '')
    file_name = os.path.join(location, os.listdir(location)[0])

    # sqldump
    wd = os.getcwd()
    os.chdir(sql_dump)
    subprocess.Popen(f'mysql -u{user} -p{password} {database} < {file_name}', shell=True).wait()

    os.chdir(wd)

    # Page
    return render(request, 'backups/finishedProcess.html', context={'message': 'Se ha restaurado la base de datos'})


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


### AUXILIAR FUNCTIONS ###
def isValidDate(date):
    try:
        if date != '':
            return  (   len(date) == 10 and
                        date[0].isdigit() and date[1].isdigit() and date[2] == '/' and
                        date[3].isdigit() and date[4].isdigit() and date[5] == '/' and
                        date[6].isdigit() and date[7].isdigit() and date[8].isdigit() and date[9].isdigit() and
                        int(date[0]+date[1]) in range(1,31) and int(date[3]+date[4]) in range(1,12)
                    )
        return False
    except:
        return False

def dateFormat(date):
    try:
        return date[6]+date[7]+date[8]+date[9]+'-'+date[3]+date[4]+'-'+date[0]+date[1]
    except:
        return ''

def isValidDateTime(date):
    try:
        if date != '':
            return  (   len(date) == 16 and
                        date[0].isdigit() and date[1].isdigit() and date[2] == '/' and
                        date[3].isdigit() and date[4].isdigit() and date[5] == '/' and
                        date[6].isdigit() and date[7].isdigit() and date[8].isdigit() and date[9].isdigit() and
                        int(date[0]+date[1]) in range(1,32) and int(date[3]+date[4]) in range(1,13) and
                        date[10] == ' ' and date[11].isdigit() and date[12].isdigit() and
                        date[13] == ':' and date[14].isdigit() and date[15].isdigit() and
                        int(date[11]+date[12]) in range(0,24) and int(date[14]+date[15]) in range(0,60)
                    )
        return False
    except:
        return False

def dateTimeFormat(date):
    try:
        return date[6]+date[7]+date[8]+date[9]+'-'+date[3]+date[4]+'-'+date[0]+date[1]+' '+date[11]+date[12]+':'+date[14]+date[15]
    except:
        return ''
    
def showDate(date):
    date = str(date)
    return date[8]+date[9]+'/'+date[5]+date[6]+'/'+date[0]+date[1]+date[2]+date[3]

def showDateTime(date):
    date = str(date)
    return date[8]+date[9]+'/'+date[5]+date[6]+'/'+date[0]+date[1]+date[2]+date[3]+' '+date[11]+date[12]+':'+date[14]+date[15]


### FIRST PART ###

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


### LAB STORAGES ###
@csrf_protect
@login_required
def createLabStorage(request):
    return createGeneric(request, LabStorageForm, 'core:createLabStorage', 'Nuevo almacén')

@csrf_protect
@login_required
def editLabStorage(request, pk):
    return editGeneric(request, LabStorageForm, pk, 'core:editLabStorage', 'Editar almacén')

@csrf_protect
@login_required
def deleteLabStorage(request, pk):
    return deleteGeneric(request, LabStorageForm, pk, 'core:deleteLabStorage', 'Borrar almacén')

@csrf_protect
@login_required
def labStorages(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    labStorages = LabStorage.objects.filter(name__icontains=query_generic).order_by('name')
    # Paginator
    paginator = Paginator(labStorages, N)
    page = request.GET.get('page', 1)
    try:
        labStorages = paginator.page(page)
    except EmptyPage:
        labStorages = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'labStorages': labStorages,
        'query_generic': query_generic,
    }
    return render(request, 'masterViewers/labStorages.html', context=ctx)


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
@csrf_protect
@login_required
def createStoragedDrug(request, storage):
    if request.method == 'POST':
        form = StoragedDrugForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            actualDrugsInStorage = []
            for drug in StoragedDrug.objects.filter(storage=storage):
                actualDrugsInStorage += drug.drug

            if form.drug in actualDrugsInStorage:
                object = StoragedDrug.objects.filter( Q(drug=form.drug) & Q(storage=storage))
                object.quantity += form.quantity
                form.save()
            else:
                form.storage = get_object_or_404(Storage, pk=storage)
                form.save()
            
        return redirect('core:storagedDrugs')
    else:
        form = StoragedDrugForm()
    
    ctx = {
        'form': form,
        'title': 'Añadir medicamento al almacén '+get_object_or_404(Storage, pk=storage).name,
        'back_url': 'core:storagedDrugs',
        'function_url': 'core:createStoragedDrug',
        'backendURL': urls.backendURL,
        'storage': storage,
        'types': DrugType.objects.all(),
    }
    return render(request, 'forms/storagedDrugForm.html', context=ctx)

@csrf_protect
@login_required
def editStoragedDrug(request, pk):
    object = get_object_or_404(StoragedDrug, pk=pk)
    if request.method == 'POST':
        form = StoragedDrugFormEdition(request.POST, instance=object)
        if form.is_valid():
            form = form.save(commit=False)
            if form.quantity <= 0:
                object.delete()
            else:
                form.save()
            return redirect('core:storagedDrugs')
    else:
        form = StoragedDrugFormEdition(instance=object)
    
    ctx = {
        'form': form,
        'title': 'Modificar cantidad o caducidad',
        'back_url': 'core:storagedDrugs',
        'function_url': 'core:editStoragedDrug',
        'pk': pk,
        'drug': object.drug,
        'storage': object.storage,
    }
    return render(request, 'forms/storagedDrugFormEdition.html', context=ctx)


@csrf_protect
@login_required
def storagedDrugs(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    query_type = request.GET.get('query_type', '0')
    query_storage = request.GET.get('query_storage', '')
    query_date_1 = request.GET.get('query_date_1', '')
    query_date_2 = request.GET.get('query_date_2', '')
    storagedDrugs = StoragedDrug.objects.filter( drug__name__icontains=query_generic ).order_by('drug__name')
    if query_storage != '':
        storagedDrugs = storagedDrugs.filter( storage__exact=query_storage )
        query_storage = int(query_storage)
    if query_type != '0':
        storagedDrugs = storagedDrugs.filter( drug__drugType=query_type )
    if isValidDate(query_date_1) and isValidDate(query_date_2):
        storagedDrugs = storagedDrugs.filter(expirationDate__range=[dateFormat(query_date_1), dateFormat(query_date_2)])
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
        'query_type': int(query_type),
        'query_storage': query_storage,
        'query_date_1': query_date_1,
        'query_date_2': query_date_2,
        'types': DrugType.objects.all(),
        'storages': Storage.objects.all(),
        'backendURL': urls.backendURL,
    }
    return render(request, 'functionalities/storagedDrugs.html', context=ctx)


@csrf_protect
@login_required
def consumeStoragedDrug(request, pk):
    storagedDrug = get_object_or_404(StoragedDrug, pk=pk)
    if storagedDrug.quantity > 1:
        storagedDrug.quantity -= 1
        storagedDrug.save()
    else:
        storagedDrug.delete()
    return redirect('core:storagedDrugs')


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
    query_date_1 = request.GET.get('query_date_1', '')
    query_date_2 = request.GET.get('query_date_2', '')
    query_status = request.GET.get('query_status', '0')
    patients = Patient.objects.filter(name__icontains=query_generic).order_by('name')
    if(query_status != '0'):
        if(query_status == '1'):
            patients = patients.exclude(admissionDate=None)
        else:
            patients = patients.filter(admissionDate=None)
    if(query_doctor != '0'):
        patients = patients.filter(doctor__exact=query_doctor)
    if(query_bed != '0'):
        patients = patients.filter(bed__exact=query_bed)
    if isValidDate(query_date_1) and isValidDate(query_date_2):
        patients = patients.filter(admissionDate__range=[dateFormat(query_date_1), dateFormat(query_date_2)])
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
        'query_generic': query_generic,
        'query_doctor': int(query_doctor),
        'query_bed': int(query_bed),
        'query_floor': query_floor,
        'query_service': int(query_service),
        'query_date_1': query_date_1,
        'query_date_2': query_date_2,
        'query_status': int(query_status),
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


### SECOND PART ###

### MASTER ###

### LAB MATERIAL ###
@csrf_protect
@login_required
def createLabMaterial(request):
    return createGeneric(request, LabMaterialForm, 'core:createLabMaterial', 'Nuevo material de laboratorio')

@csrf_protect
@login_required
def editLabMaterial(request, pk):
    return editGeneric(request, LabMaterialForm, pk, 'core:editLabMaterial', 'Editar material de laboratorio')

@csrf_protect
@login_required
def deleteLabMaterial(request, pk):
    return deleteGeneric(request, LabMaterialForm, pk, 'core:deleteLabMaterial', 'Borrar material de laboratorio')

@csrf_protect
@login_required
def labMaterials(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    query_type = request.GET.get('query_type', '0')
    labMaterials = LabMaterial.objects.filter(name__icontains=query_generic).order_by('name')
    if query_type != '0':
        labMaterials = labMaterials.filter(materialType=query_type)
    # Paginator
    paginator = Paginator(labMaterials, N)
    page = request.GET.get('page', 1)
    try:
        labMaterials = paginator.page(page)
    except EmptyPage:
        labMaterials = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'labMaterials': labMaterials,
        'types': materialTypes.items(),
        'query_generic': query_generic,
        'query_type': query_type,
    }
    return render(request, 'masterViewers/labMaterials.html', context=ctx)


### STORAGED LAB MATERIAL ###
@csrf_protect
@login_required
def createStoragedLabMaterial(request, storage):
    if request.method == 'POST':
        form = StoragedLabMaterialForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            actualLabMaterialsInStorage = []
            for labMaterial in StoragedLabMaterial.objects.filter(storage=storage):
                actualLabMaterialsInStorage += labMaterial.labMaterial

            if form.labMaterial in actualLabMaterialsInStorage:
                obj = StoragedLabMaterial.objects.filter(Q(labMaterial=form.labMaterial) & Q(storage=storage))
                obj.quantity += form.quantity
                form.save()
            else:
                form.storage = get_object_or_404(Storage, pk=storage)
                form.save()

            return redirect('core:storagedLabMaterials')
    else:
        form = StoragedLabMaterialForm()

    ctx = {
        'form': form,
        'title': 'Añadir material de laboratorio al almacén ' + get_object_or_404(Storage, pk=storage).name,
        'back_url': 'core:storagedLabMaterials',
        'function_url': 'core:createStoragedLabMaterial',
        'backendURL': urls.backendURL,
        'storage': storage,
        'types': materialTypes.items(),
    }
    return render(request, 'forms/storagedLabMaterialForm.html', context=ctx)


@csrf_protect
@login_required
def editStoragedLabMaterial(request, pk):
    obj = get_object_or_404(StoragedLabMaterial, pk=pk)
    if request.method == 'POST':
        form = StoragedLabMaterialFormEdition(request.POST, instance=obj)
        if form.is_valid():
            form = form.save(commit=False)
            if form.quantity <= 0:
                obj.delete()
            else:
                form.save()
            return redirect('core:storagedLabMaterials')
    else:
        form = StoragedLabMaterialFormEdition(instance=obj)

    ctx = {
        'form': form,
        'title': 'Modificar cantidad',
        'back_url': 'core:storagedLabMaterials',
        'function_url': 'core:editStoragedLabMaterial',
        'pk': pk,
        'labMaterial': obj.labMaterial,
        'storage': obj.storage,
    }
    return render(request, 'forms/storagedLabMaterialFormEdition.html', context=ctx)


@csrf_protect
@login_required
def storagedLabMaterials(request):
    # Queries
    query_generic = request.GET.get('query_generic', '')
    query_type = request.GET.get('query_type', '0')
    query_storage = request.GET.get('query_storage', '')
    storagedLabMaterials = StoragedLabMaterial.objects.filter(labMaterial__name__icontains=query_generic).order_by('labMaterial__name')
    
    if query_storage != '':
        storagedLabMaterials = storagedLabMaterials.filter(storage=query_storage)
        query_storage = int(query_storage)
    
    if query_type != '0':
        storagedLabMaterials = storagedLabMaterials.filter(labMaterial__labMaterialType=query_type)
    
    # Paginator
    paginator = Paginator(storagedLabMaterials, N)
    page = request.GET.get('page', 1)
    try:
        storagedLabMaterials = paginator.page(page)
    except EmptyPage:
        storagedLabMaterials = paginator.page(paginator.num_pages)

    # Render
    ctx = {
        'storagedLabMaterials': storagedLabMaterials,
        'query_generic': query_generic,
        'query_type': int(query_type),
        'query_storage': query_storage,
        'types': materialTypes.items(),
        'storages': Storage.objects.all(),
        'backendURL': urls.backendURL,
    }
    return render(request, 'functionalities/storagedLabMaterials.html', context=ctx)


@csrf_protect
@login_required
def consumeStoragedLabMaterial(request, pk):
    storagedLabMaterial = get_object_or_404(StoragedLabMaterial, pk=pk)
    if storagedLabMaterial.quantity > 1:
        storagedLabMaterial.quantity -= 1
        storagedLabMaterial.save()
    else:
        storagedLabMaterial.delete()
    
    return redirect('core:storagedLabMaterials')


### SAMPLES ###
@csrf_protect
@login_required
def createSample(request, storage):
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.storage = get_object_or_404(LabStorage, pk=storage)
            form.save()
            return redirect('core:sampleID', form.pk)
    else:
        form = SampleForm()
    ctx = {
        'form': form,
        'title': 'Añadir muestra al almacén ' + get_object_or_404(LabStorage, pk=storage).name,
        'back_url': 'core:samples',
        'function_url': 'core:createSample',
        'backendURL': urls.backendURL,
        'storage': storage,
    }
    return render(request, 'forms/sampleForm.html', context=ctx)


@csrf_protect
@login_required
def sampleID(request, pk):
    ctx = {
        'pk': pk,
        'object_type': 'muestra',
        'object_type_rec': 'muestra',
        'back_url': 'core:samples',
    }
    return render(request, 'forms/generatedCode.html', context=ctx)

@csrf_protect
@login_required
def editSample(request, pk):
    object = get_object_or_404(Sample, pk=pk)
    if request.method == 'POST':
        form = SampleFormEdition(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect(SampleForm.Meta.redirect_url)
    else:
        form = SampleFormEdition(instance=object)
    
    ctx = {
        'form': form,
        'title': 'Editar datos de muestra',
        'back_url': SampleFormEdition.Meta.redirect_url,
        'function_url': 'core:editSample',
        'pk': pk,
        'sampleType': object.verbose_sampleType,
        'storage': object.storage,
        'patient': object.patient,
        'date': object.date,
    }
    return render(request, 'forms/sampleFormEdition.html', context=ctx)


@csrf_protect
@login_required
def deleteSample(request, pk):
    return deleteGeneric(request, SampleForm, pk, 'core:deleteSample', 'Descartar muestra')


@csrf_protect
@login_required
def samples(request):
    # Queries
    query_type = request.GET.get('query_type', '0')
    query_patient = request.GET.get('query_patient', '')
    query_date_1 = request.GET.get('query_date_1', '')
    query_date_2 = request.GET.get('query_date_2', '')
    query_storage = request.GET.get('query_storage', '')
    samples = Sample.objects.all().order_by('-date')
    allSamples = samples
    if query_storage != '':
        samples = samples.filter( storage=query_storage )
        query_storage = int(query_storage)
    if query_type != '0':
        samples = samples.filter(Q(sampleType=query_type))
    if query_patient != '':
        samples = samples.filter(Q(patient__name__icontains=query_patient) | (Q(patient__historyNumber__icontains=query_patient)))
    if isValidDateTime(query_date_1) and isValidDateTime(query_date_2):
        samples = samples.filter(date__range=[dateTimeFormat(query_date_1), dateTimeFormat(query_date_2)])
    # Paginator
    paginator = Paginator(samples, N)
    page = request.GET.get('page', 1)
    try:
        samples = paginator.page(page)
    except EmptyPage:
        samples = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'allSamples': allSamples,
        'samples': samples,
        'query_type': query_type,
        'query_patient': query_patient,
        'query_date_1': query_date_1,
        'query_date_2': query_date_2,
        'query_storage': query_storage,
        'types': sampleTypes.items(),
        'storages': LabStorage.objects.all(),
        'backendURL': urls.backendURL,
    }
    return render(request, 'functionalities/samples.html', context=ctx)


### BLOOD ###
@csrf_protect
@login_required
def createBlood(request, storage):
    if request.method == 'POST':
        form = BloodForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.storage = get_object_or_404(LabStorage, pk=storage)
            form.save()
            return redirect('core:bloodID', form.pk)
    else:
        form = BloodForm()
    ctx = {
        'form': form,
        'title': 'Añadir bolsa de sangre a ' + get_object_or_404(LabStorage, pk=storage).name,
        'back_url': 'core:blood',
        'function_url': 'core:createBlood',
        'backendURL': urls.backendURL,
        'storage': storage,
    }
    return render(request, 'forms/bloodForm.html', context=ctx)


@csrf_protect
@login_required
def bloodID(request, pk):
    ctx = {
        'pk': pk,
        'object_type': 'bolsa de sangre',
        'object_type_rec': 'bolsa',
        'back_url': 'core:blood',
    }
    return render(request, 'forms/generatedCode.html', context=ctx)


@csrf_protect
@login_required
def editBlood(request, pk):
    object = get_object_or_404(Blood, pk=pk)
    if request.method == 'POST':
        form = BloodFormEdition(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect(BloodFormEdition.Meta.redirect_url)
    else:
        form = BloodFormEdition(instance=object)
    
    ctx = {
        'form': form,
        'title': 'Reservar / Trasladar / Añadir pruebas a bolsa' + str(pk),
        'back_url': BloodFormEdition.Meta.redirect_url,
        'function_url': 'core:editBlood',
        'pk': pk,
        'verbose_type': bloodGroups[object.bloodGroup],
        'date': object.date,
        'verbose_process': object.verbose_process,
        'capacity': object.capacity,
    }
    return render(request, 'forms/bloodFormEdition.html', context=ctx)


@csrf_protect
@login_required
def deleteBlood(request, pk):
    object = get_object_or_404(Blood, pk=pk)
    if request.method == 'POST':
        object.delete()
        return redirect('core:blood')

    ctx = {
        'object': object,
        'pk': pk,
    }
    return render(request, 'forms/bloodDeletion.html', context=ctx)

@csrf_protect
@login_required
def blood(request):
    # Queries
    query_type = request.GET.get('query_type', '0')
    query_patient = request.GET.get('query_patient', '')
    query_date_1 = request.GET.get('query_date_1', '')
    query_date_2 = request.GET.get('query_date_2', '')
    query_process = request.GET.get('query_process', '0')
    query_storage = request.GET.get('query_storage', '')
    bloodBags = Blood.objects.all().order_by('-date')
    allBloodBags = bloodBags
    if query_storage != '':
        bloodBags = bloodBags.filter( storage=query_storage )
        query_storage = int(query_storage)
    if query_type != '0':
        bloodBags = bloodBags.filter(bloodGroup=query_type)
    if query_patient != '':
        bloodBags = bloodBags.filter(Q(reserved__name__icontains=query_patient) | (Q(reserved__historyNumber__icontains=query_patient)))
    if query_process != '0':
        bloodBags = bloodBags.filter(process=query_process)
    if isValidDateTime(query_date_1) and isValidDateTime(query_date_2):
        bloodBags = bloodBags.filter(date__range=[dateTimeFormat(query_date_1), dateTimeFormat(query_date_2)])
    # Paginator
    paginator = Paginator(bloodBags, N)
    page = request.GET.get('page', 1)
    try:
        bloodBags = paginator.page(page)
    except EmptyPage:
        bloodBags = paginator.page(paginator.num_pages)
    # Render
    ctx = {
        'allBloodBags': allBloodBags,
        'blood': bloodBags,
        'query_type': query_type,
        'query_patient': query_patient,
        'query_date_1': query_date_1,
        'query_date_2': query_date_2,
        'query_storage': query_storage,
        'query_process': query_process,
        'types': bloodGroups.items(),
        'processes': processTypes.items(),
        'storages': LabStorage.objects.all(),
        'backendURL': urls.backendURL,
    }
    return render(request, 'functionalities/blood.html', context=ctx)


### BACKEND FUNCTIONS ###
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
@login_required
def filterByGroup(request, group):
    if request.method == 'GET':
        drugs = Drug.objects.all()
        if(group != 0): drugs = drugs.filter(drugType__exact=group)
        result = []
        for drug in drugs:
            result.append({'key': drug.pk, 'value': drug.name})
        return JsonResponse({'result': result})
    else:
        return JsonResponse({})
    
@csrf_protect
@login_required
def filterByType(request, type):
    if request.method == 'GET':
        labMaterials = LabMaterial.objects.all()
        if type != 0:
            labMaterials = labMaterials.filter(materialType__exact=type)
        result = []
        for labMaterial in labMaterials:
            result.append({'key': labMaterial.pk, 'value': labMaterial.name})
        
        return JsonResponse({'result': result})
    else:
        return JsonResponse({})

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

@csrf_protect
@login_required
def viewStoragedDrug(request, pk):
    if request.method == 'GET':

        storagedDrug = get_object_or_404(StoragedDrug, pk=pk)
        
        return JsonResponse({
                                'BackendStoragedDrug_name': storagedDrug.drug.name,
                                'BackendStoragedDrug_NDC': storagedDrug.drug.verbose_NDC,
                                'BackendStoragedDrug_drugType': str(storagedDrug.drug.verbose_drugType),
                                'BackendStoragedDrug_storage': storagedDrug.storage.name,
                                'BackendStoragedDrug_quantity': storagedDrug.quantity,
                                'BackendStoragedDrug_expirationDate': storagedDrug.verbose_expirationDate,
                                'BackendStoragedDrug_total': storagedDrug.drug.total,
                            })
    else:
        return JsonResponse({})
    
@csrf_protect
@login_required
def viewStoragedLabMaterial(request, pk):
    if request.method == 'GET':

        storagedLabMaterial = get_object_or_404(StoragedLabMaterial, pk=pk)
        
        return JsonResponse({
                                'BackendStoragedLabMaterial_material': storagedLabMaterial.labMaterial.name,
                                'BackendStoragedLabMaterial_type': storagedLabMaterial.labMaterial.verbose_materialType,
                                'BackendStoragedLabMaterial_storage': storagedLabMaterial.storage.name,
                                'BackendStoragedLabMaterial_quantity': storagedLabMaterial.quantity,
                                'BackendStoragedLabMaterial_total': storagedLabMaterial.labMaterial.total,
                            })
    else:
        return JsonResponse({})
    
@csrf_protect
@login_required
def viewSample(request, pk):
    if request.method == 'GET':

        sample = get_object_or_404(Sample, pk=pk)
        
        return JsonResponse({
                                'BackendSample_pk': sample.pk,
                                'BackendSample_patient': sample.patient.name,
                                'BackendSample_type': sample.verbose_sampleType,
                                'BackendSample_date': showDateTime(sample.date),
                                'BackendSample_storage': sample.storage.name,
                                'BackendSample_expirationDate': showDate(sample.expirationDate),
                                'BackendSample_data': sample.data,
                            })
    else:
        return JsonResponse({})
    
@csrf_protect
@login_required
def viewBlood(request, pk):
    if request.method == 'GET':

        blood = get_object_or_404(Blood, pk=pk)
        
        return JsonResponse({
                                'BackendBlood_pk': blood.pk,
                                'BackendBlood_patient': blood.verbose_patient,
                                'BackendBlood_type': bloodGroups[blood.bloodGroup],
                                'BackendBlood_date': showDateTime(blood.date),
                                'BackendBlood_storage': blood.storage.name,
                                'BackendBlood_expirationDate': showDate(blood.expirationDate),
                                'BackendBlood_capacity': blood.capacity,
                                'BackendBlood_process': processTypes[blood.process],
                            })
    else:
        return JsonResponse({})
    
@csrf_protect
@login_required
def getAllBlood(request):
    if request.method == 'GET':

        view_Ap, view_Am, view_Bp, view_Bm, view_ABp, view_ABm, view_Op, view_Om = 0, 0, 0, 0, 0, 0, 0, 0
        blood = Blood.objects.filter(reserved__isnull=True).order_by('-date')

        for bag in blood:
            if bag.bloodGroup == '1':
                view_Ap += bag.capacity
            elif bag.bloodGroup == '2':
                view_Am += bag.capacity
            elif bag.bloodGroup == '3':
                view_Bp += bag.capacity
            elif bag.bloodGroup == '4':
                view_Bm += bag.capacity
            elif bag.bloodGroup == '5':
                view_ABp += bag.capacity
            elif bag.bloodGroup == '6':
                view_ABm += bag.capacity
            elif bag.bloodGroup == '7':
                view_Op += bag.capacity
            elif bag.bloodGroup == '8':
                view_Om += bag.capacity

        return JsonResponse({
                                'view_Ap': view_Ap/1000, 'view_Am': view_Am/1000, 'view_Bp': view_Bp/1000, 'view_Bm': view_Bm/1000,
                                'view_ABp': view_ABp/1000, 'view_ABm': view_ABm/1000, 'view_Op': view_Op/1000, 'view_Om': view_Om/1000,
                            })
    else:
        return JsonResponse({})