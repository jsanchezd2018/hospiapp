from django.urls import include, path
from . import views

app_name = 'core'
backendURL = 'http://127.0.0.1:8000/'


### PHYSICAL PLACES ###
storage_patterns = [
    path('', views.storages, name='storages'),
    path('crear', views.createStorage, name='createStorage'),
    path('editar/<int:pk>', views.editStorage, name='editStorage'),
    path('eliminar/<int:pk>', views.deleteStorage, name='deleteStorage'),
]

labStorage_patterns = [
    path('', views.labStorages, name='labStorages'),
    path('crear', views.createLabStorage, name='createLabStorage'),
    path('editar/<int:pk>', views.editLabStorage, name='editLabStorage'),
    path('eliminar/<int:pk>', views.deleteLabStorage, name='deleteLabStorage'),
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
    path('asignar/<int:user_pk>', views.setRole, name='setRole'),
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


### LAB ###
labMaterial_patterns = [
    path('', views.labMaterials, name='labMaterials'),
    path('crear/', views.createLabMaterial, name='createLabMaterial'),
    path('editar/<int:pk>', views.editLabMaterial, name='editLabMaterial'),
    path('eliminar/<int:pk>', views.deleteLabMaterial, name='deleteLabMaterial'),
]

storagedLabMaterial_patterns = [
    path('', views.storagedLabMaterials, name='storagedLabMaterials'),
    path('crear/<int:storage>', views.createStoragedLabMaterial, name='createStoragedLabMaterial'),
    path('editar/<int:pk>', views.editStoragedLabMaterial, name='editStoragedLabMaterial'),
    path('consumir/<int:pk>', views.consumeStoragedLabMaterial, name='consumeStoragedLabMaterial'),
]

sample_patterns = [
    path('', views.samples, name='samples'),
    path('crear/<int:storage>', views.createSample, name='createSample'),
    path('codigo/<int:pk>', views.sampleID, name='sampleID'),
    path('editar/<int:pk>', views.editSample, name='editSample'),
    path('borrar/<int:pk>', views.deleteSample, name='deleteSample'),
]

blood_patterns = [
    path('', views.blood, name='blood'),
    path('crear/<int:storage>', views.createBlood, name='createBlood'),
    path('codigo/<int:pk>', views.bloodID, name='bloodID'),
    path('editar/<int:pk>', views.editBlood, name='editBlood'),
    path('borrar/<int:pk>', views.deleteBlood, name='deleteBlood'),
]


### BACKUPS ###
backups_patterns = [
    path('', views.backups, name='backups'),
    path('crear_copia/', views.createBackup, name='createBackup'),
    path('restaurar/', views.restoreBackup, name='restoreBackup'),
]

### URL PATTERNS ###

urlpatterns = [
    # Index
    path('', views.index, name='index'),
    path('permiso_denegado', views.denied, name='denied'),
    # physical places
    path('almacenes/', include(storage_patterns)),
    path('almacenes_laboratorio/', include(labStorage_patterns)),
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
    # lab
    path('materiales/', include(labMaterial_patterns)),
    path('laboratorio/', include(storagedLabMaterial_patterns)),
    path('muestras/', include(sample_patterns)),
    path('sangre/', include(blood_patterns)),
    # login / logout
    path('accounts/login/', views.userLogin, name='userLogin'),
    path('logout/', views.userLogout, name='userLogout'),
    # backups
    path('copias_de_seguridad/', include(backups_patterns)),
    # backend functions
    path('filter/<int:pk_service>/<int:floor>/<int:pk_patient>', views.filter, name='filter'),
    path('filterByGroup/<int:group>', views.filterByGroup, name='filterByGroup'),
    path('filterByType/<int:type>', views.filterByType, name='filterByType'),
    path('filterInManagement/<int:pk_service>/<int:floor>', views.filterInManagement, name='filterInManagement'),
    path('viewPatient/<int:pk>', views.viewPatient, name='viewPatient'),
    path('viewStoragedDrug/<int:pk>', views.viewStoragedDrug, name='viewStoragedDrug'),
    path('viewStoragedLabMaterial/<int:pk>', views.viewStoragedLabMaterial, name='viewStoragedLabMaterial'),
    path('viewSample/<int:pk>', views.viewSample, name='viewSample'),
    path('viewBlood/<int:pk>', views.viewBlood, name='viewBlood'),
    path('getAllBlood/', views.getAllBlood, name='getAllBlood'),
]

