from django.urls import include, path
from . import views

app_name = 'core'

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

urlpatterns = [
    path('', views.index, name='index'),
    path('medicamentos/', include(drug_patterns)),
    path('grupos/', include(drugType_patterns)),
    
]