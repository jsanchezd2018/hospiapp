from django.contrib import admin

from .models import *

admin.site.register(Storage)
admin.site.register(Service)
admin.site.register(Bed)
admin.site.register(DrugType)
admin.site.register(Drug)
admin.site.register(StoragedDrug)
admin.site.register(Doctor)
admin.site.register(User)
admin.site.register(Patient)


