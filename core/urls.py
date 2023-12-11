from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'core'

drug_patterns = [
    path('', views.drugs, name='drugs'),
    path('crear/', views.createDrug, name='createDrug'),
    path('editar/<int:pk>', views.editDrug, name='editDrug'),
    path('eliminar/<int:pk>', views.deleteDrug, name='deleteDrug'),
]

'''drugType_patterns = [
    path('', views.drugTypes, name='tipos'),
    path('crear', views.createDrugType, name='crear_tipo'),
    path('editar/<int:pk>', views.createDrugType, name='editar_tipo'),
    path('eliminar/<int:pk>', views.createDrugType, name='eliminar_tipo'),
]'''

urlpatterns = [
    path("", views.index, name="index"),
    path('medicamentos/', include(drug_patterns)),
    #path('drugTypes/', include(drug_patterns)),
    
]