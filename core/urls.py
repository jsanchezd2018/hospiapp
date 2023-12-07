from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'core'

drug_patterns = [
    path('', views.drugs, name='medicamentos'),
    path('crear/', views.createDrug, name='crear_medicamento'),
    path('editar/<int:pk>', views.editDrug, name='editar_medicamento'),
    path('eliminar/<int:pk>', views.deleteDrug, name='eliminar_medicamento'),
]

'''drugType_patterns = [
    path('', views.drugTypes, name='tipos'),
    path('crear', views.createDrugType, name='crear_tipo'),
    path('editar/<int:pk>', views.createDrugType, name='editar_tipo'),
    path('eliminar/<int:pk>', views.createDrugType, name='eliminar_tipo'),
]'''

urlpatterns = [
    path("", views.index, name="index"),
    path('drugs/', include(drug_patterns)),
    #path('drugTypes/', include(drug_patterns)),
    
]