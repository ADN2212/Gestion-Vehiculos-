from django.contrib import admin
from gestion_vehiculos_api.models import Vehiculo, Viaje, Chofer, GVUser

class Administrador_vehiculos(admin.ModelAdmin):
	list_display = ('id_vehiculo', 'marca', 'placa', 'tipo_servicio')
	#search_fields = ('placa', 'marca')
	list_filter = ('tipo_servicio',)#Permitira que se hagan filtros por ese campo.


admin.site.register(Vehiculo, Administrador_vehiculos)
admin.site.register(Viaje)
admin.site.register(Chofer)
admin.site.register(GVUser)
















