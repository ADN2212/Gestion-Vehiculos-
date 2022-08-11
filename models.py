from django.db import models
#from django.contrib.auth.models import User

class Vehiculo(models.Model):
	"""
	Tabla para almacenar la informacion concerniente a los Omnibus de la empresa.
	"""		
	id_vehiculo = models.AutoField(primary_key = True)#Declarar la pk de forma explicita.	
	
	placa = models.CharField(max_length = 7, unique = True, default = None)#Una placa de autobus privado esta compuesta por "I" + "num", donde num es un int en [0, 999999] 
	
	marca = models.CharField(max_length = 100, default = None)
	
	peso_en_toneladas = models.DecimalField(max_digits = 5, decimal_places = 2, default = None, verbose_name = 'Peso en Toneladas')#Seria mejor que fuera un PositiveSmallIntegerField?
	
	COMBUSTIBLES =	(
						('Gasolina', 'Gasolina'), 
						('Diesel', 'Diesel'),
						('Petroleo', 'Petroleo')
					)
	
	tipo_de_comnustible = models.CharField(max_length = 8, choices = COMBUSTIBLES, default = None, verbose_name = 'Tipo de Combustible')	
	
	kms_recorridos = models.PositiveIntegerField(default = 0, verbose_name = 'Kilometros Recorridos')
	
	velocidad_maxima = models.PositiveSmallIntegerField(default = 0, verbose_name = 'Velocidad Máxima (km/h)')#Se pueden agregar cotas.
	
	agnos_explotacion = models.PositiveSmallIntegerField(default = 0, null = True, verbose_name = 'Años de Explotación') 
	
	SERVICIOS = (
					('Regular', 'Regular'),
					('Especial', 'Especial'),
					('VIP', 'VIP')
				)
	
	tipo_servicio = models.CharField(max_length = 8, choices = SERVICIOS, default = None, verbose_name = 'Tipo de Servicio')
	
	climatizacion = models.BooleanField(default = None, verbose_name = 'Tiene aire acondicionado?')#True or False.
	
	cantidad_asientos = models.IntegerField(default = None, verbose_name = 'Cuantos asientos tiene?')
	
	disponibilidad = models.BooleanField(default = None, verbose_name = 'Está disponible?')

	class Meta:
		db_table = 'Vehiculos'

	#representacion del objeto en cadena de textp
	def __str__(self):
	
		return 	'Onmibus de Marca: {}, Placa número: {} y Tipo de Servicio: {}'.format(self.marca, self.placa, self.tipo_servicio)

		#return 'Omnibus'#Si se espefican la 'list_display' este metodo no tendrá efecto.


class DatosPersona(models.Model):
	"""
	Clase para aplicar herencia obstracta a las tablas Chofer y GVUser
	Esta tabla no será nesesaria a futuro, dado que GVUser no 'estara'
	"""	
	nombre_completo = models.CharField(default = '', max_length = 100, verbose_name = 'Nombre Completo')
	
	cedula = models.CharField(default = None, max_length = 30, unique = True, verbose_name = 'Cedula')#Las cedulas son identificadores unicos.
	
	edad = models.PositiveSmallIntegerField(default = 18, verbose_name = 'Edad')
	
	numero_telefono = models.CharField(default = None, max_length = 20, verbose_name = 'Número de Telefono')#Deberia ser unico?
	
	direccion_particular = models.CharField(default = 'Somewhere', max_length = 150, verbose_name = 'Reside en')
	
	email = models.EmailField(default = 'SomeOne@gamil.com', null = True, blank = True)#Este campo verifica que sea un email valido, en caso de que no, lanza un error.
	#Email deberia ser unico?

	class Meta:
		abstract = True

class Chofer(DatosPersona):
	"""
	Clase que modela la tabla que contedrá los choferes en la Base de Datos.	
	"""
	id_chofer = models.AutoField(primary_key = True)

	NIVELES_ECOLARES =	(
							('Inicial', 'Inicial'),
							('Primaria', 'Primaria'),
							('Secundaria', 'Secundaria'),
							('Superior', 'Superior')
						)

	nivel_escolar = models.CharField(max_length = 10, choices = NIVELES_ECOLARES, verbose_name = 'Cual es su nivel escolar?')

	SEXOS =	(
				('Masculino', 'Masculino'),
				('Femenino', 'Femenino')				
			)

	sexo = models.CharField(default = None, max_length = 10, choices = SEXOS, verbose_name = 'Elija un Sexo')

	agnos_experiencia = models.PositiveSmallIntegerField(default = 0, verbose_name = 'Cuantos años de experiencia tiene?')

	cantidad_de_multas = models.PositiveSmallIntegerField(default = 0, verbose_name = 'Cantidad de Multas')

	CLASIFICACIONES =	(
							('A', 'A'),
							('B', 'B')
						)

	clasificacion = models.CharField(default = None, max_length = 1, choices = CLASIFICACIONES, verbose_name = 'Clasificación de Tipo')

	class Meta:
		db_table = 'Coferes'

	def __str__(self):

		return 'Chofer: {} de {} años, cedula: {} y tel: {}'.format(self.nombre_completo, self.edad, self.cedula, self.numero_telefono)


class Viaje(models.Model):
	"""
	Clase que modela la tabla que contedrá los viejas en la Base de Datos.
	"""

	id_viaje = models.AutoField(primary_key = True)
	
	TIPOS_DE_VIAJE =	(
							('Local', 'Local'),
							('Municipal', 'Municipla'),
							('Provincial', 'Provincial'),
							('Turismo', 'Turismo'),
							('Arrendado', 'Arrendado'),
						)
	tipo_viaje = models.CharField(max_length = 10, choices = TIPOS_DE_VIAJE, verbose_name = 'Tipo de Viaje')

	inicio_viaje = models.DateTimeField(default = None, verbose_name = 'Inicio del Viaje')#Usar DateTimeField seria mas presiso.

	fin_viaje = models.DateTimeField(default = None, verbose_name = 'Fin del Viaje')

	kms_recorridos = kms_recorridos = models.PositiveIntegerField(default = 0, verbose_name = 'Kilometros Recorridos en el Viaje')

	comentarios = models.TextField(default = '...', verbose_name = 'Haga un Comentario')

	vehiculo = models.ForeignKey(Vehiculo, on_delete = models.SET_NULL, null = True)#Usar on_delete = models.CASCADE ?

	chofer = models.ForeignKey(Chofer, on_delete = models.SET_NULL, null = True)

	ESTADOS_DE_VIAJE = 	(
							('Creado', 'Creado'),
							('En Proceso', 'En Proceso'),
							('Cerrado', 'Cerrado')
						)

	estado_viaje = models.CharField(default = 'Creado', max_length = 10, choices = ESTADOS_DE_VIAJE, verbose_name = 'Estado del Viaje')

	costo_usd = models.DecimalField(max_digits = 7, decimal_places = 2, default = 0, verbose_name = 'Costo del viaje en USD$')#No mostrar este campo al user cuendo se este creando el viaje.
		
	class Meta:
		db_table = 'Viajes'#Este nombre será asiganado a la tabla.

	def __str__(self):
		return 'Viaje de tipo {}'.format(self.tipo_viaje)

"""
class GVUser(DatosPersona):
	
	#Esta clase modela la tabla de los usuarios
	#Debería estar conectada a Chofer, Viaje y Vehiculo por medio de su pk?
	#Hay una manera de agregar campos extras a la tabla User que django trae por defecto. 	

	user_id = models.AutoField(primary_key = True)

	ROLES =	(
				('Administrador', 'Administrador'),
				('Agente', 'Agente'),
				('Supervisor', 'Supervisor')
			)

	rol = models.CharField(max_length = 13, choices = ROLES, verbose_name = 'Eliga el Rol de este Usuario')

	#Agregar contraseña ...

	class Meta:
		db_table = 'Usuarios Gestión Vehiculos'

	def __str__(self):
		return 'User: {}, Rol: {}'.format(self.nombre_completo, self.rol)

"""		






