from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from CustomUsers.models import SGVUser

"""
class Administrador_SGVUser(admin.ModelAdmin):
	list_filter = ('rol',)
"""

class Administrador_SGVUser(UserAdmin):
	list_display = ('email', 'id', 'username', 'nombre_completo', 'rol', 'is_admin', 'is_staff')
	search_fields = ('email', 'username')	
	list_filter = ('rol',)
	readonly_fields = ('date_joined', 'last_login')

	#Estas variables son abligatorias aunque no se vayan a usar.
	filter_horizontal = ()
	fieldsets = ()


admin.site.register(SGVUser, Administrador_SGVUser)



# Register your models here.


