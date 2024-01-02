from django.urls import include, path
from django.contrib.auth.views import LoginView

from . import views

app_name = 'core'

### PHYSICAL PLACES ###
storage_patterns = [
    path('', views.storages, name='storages'),
    path('crear', views.createStorage, name='createStorage'),
    path('editar/<int:pk>', views.editStorage, name='editStorage'),
    path('eliminar/<int:pk>', views.deleteStorage, name='deleteStorage'),
]

service_patterns = [
    path('', views.services, name='services'),
    path('crear', views.createService, name='createService'),
    path('editar/<int:pk>', views.editService, name='editService'),
    path('eliminar/<int:pk>', views.deleteService, name='deleteService'),
]

bed_patterns = [
    path('', views.beds, name='beds'),
    path('crear', views.createBed, name='createBed'),
    path('editar/<int:pk>', views.editBed, name='editBed'),
    path('eliminar/<int:pk>', views.deleteBed, name='deleteBed'),
]

### DRUGS ###
drug_patterns = [
    path('', views.drugs, name='drugs'),
    path('crear/', views.createDrug, name='createDrug'),
    path('editar/<int:pk>', views.editDrug, name='editDrug'),
    path('eliminar/<int:pk>', views.deleteDrug, name='deleteDrug'),
]

drugType_patterns = [
    path('', views.drugTypes, name='drugTypes'),
    path('crear', views.createDrugType, name='createDrugType'),
    path('editar/<int:pk>', views.editDrugType, name='editDrugType'),
    path('eliminar/<int:pk>', views.deleteDrugType, name='deleteDrugType'),
]

storagedDrug_patterns = [
    path('', views.storagedDrugs, name='storagedDrugs'),
    path('crear/<int:storage>', views.createStoragedDrug, name='createStoragedDrug'),
    path('editar/<int:pk>', views.editStoragedDrug, name='editStoragedDrug'),
    path('consumir/<int:pk>', views.consumeStoragedDrug, name='consumeStoragedDrug'),
]

### PEOPLE ###
doctor_patterns = [
    path('', views.doctors, name='doctors'),
    path('crear/', views.createDoctor, name='createDoctor'),
    path('editar/<int:pk>', views.editDoctor, name='editDoctor'),
    path('eliminar/<int:pk>', views.deleteDoctor, name='deleteDoctor'),
]

user_patterns = [
    path('', views.users, name='users'),
    path('crear/', views.createUser, name='createUser'),
    path('editar/<int:pk>', views.editUser, name='editUser'),
    path('eliminar/<int:pk>', views.deleteUser, name='deleteUser'),
]

patient_patterns = [
    path('', views.patients, name='patients'),
    path('gestion/', views.patientsManagement, name='patientsManagement'),
    path('alta/<int:pk>', views.dischargePatient, name='dischargePatient'),
    path('crear/', views.createPatient, name='createPatient'),
    path('editar/<int:pk>', views.editPatient, name='editPatient'),
    path('eliminar/<int:pk>', views.deletePatient, name='deletePatient'),
]


### URL PATTERNS ###

backendURL = 'http://127.0.0.1:8000/'

urlpatterns = [
    # Index
    path('', views.index, name='index'),
    # physical places
    path('almacenes/', include(storage_patterns)),
    path('servicios/', include(service_patterns)),
    path('camas/', include(bed_patterns)),
    # drugs
    path('medicamentos/', include(drug_patterns)),
    path('grupos/', include(drugType_patterns)),
    path('farmacia/', include(storagedDrug_patterns)),
    # people
    path('medicos/', include(doctor_patterns)),
    path('usuarios/', include(user_patterns)),
    path('pacientes/', include(patient_patterns)),

    # login / logout
    #path('login/', views.userLogin, name='userLogin'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', views.userLogout, name='userLogout'),

    # backend functions
    path('filter/<int:pk_service>/<int:floor>', views.filter, name='filter'),
    path('filterByGroup/<int:group>', views.filterByGroup, name='filterByGroup'),
    path('filterInManagement/<int:pk_service>/<int:floor>', views.filterInManagement, name='filterInManagement'),
    path('viewPatient/<int:pk>', views.viewPatient, name='viewPatient'),
    path('viewStoragedDrug/<int:pk>', views.viewStoragedDrug, name='viewStoragedDrug'),

]