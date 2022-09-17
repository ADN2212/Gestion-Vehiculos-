from django.core.exceptions import ObjectDoesNotExist
from gestion_vehiculos_api.models import Chofer, Vehiculo
from gestion_vehiculos_api.serializers import ChoferSerializer, VehiculoSerializer
from datetime import datetime as dt
#Para poder usarlo en otras funciones.
formato = '%Y-%m-%dT%H:%M:%SZ'#Debo percatarme de que las fechas entren en este formato.

def do_query(Modelo, ID = None, order_by_arg = None):
	"""
	Esta funcion se encarga de hacer las querys a la BD atrevez de los modelos y retornar los Datos conseguidos. 
	servirá para no tener que repetir el codigo de hacer las querys de manera individual en cada view de la API.
	"""
	
	if ID:
		try:
			registro = Modelo.objects.get(pk = ID)#pk se refiere a la 'Primary Key' del modelo actual.
			return registro

		except ObjectDoesNotExist:
			return None

	if order_by_arg:
		registros  = Modelo.objects.all().order_by(order_by_arg)
	
	else:
		registros = Modelo.objects.all()
		
	return registros if registros else None#Resgistro should be an empty queryset.


def add_errors(request_data, object_type):
	"""
	Prueba si hay errores espesifcos dentro del dicinario request_data,
	y los agrega en caso de.
	"""
	#print(request_data)
	#errores = {'error1': 'esto esta mal', 'error2' : 'esto tambien'}
	
	errores = {}

	if object_type == 'Chofer':

		#Para probar que la edad del chofer sea mayor a igual que 18
		edad = request_data.get('edad')
		#Para comparar con la edad 
		agnos_experiencia = request_data.get('agnos_experiencia')

		#Aqui se puede romper ...
		if edad and edad < 18:
			errores['error_edad'] = ['La edad debe ser mayor o igaual a 18.']#una lista para mostrarlo como lo muestra el framework.
		
		"""
		#Para solicitar un minimo de años de experiencia:
		if edad and agnos_experiencia:
			if not (edad - agnos_experiencia >= 18):
				errores['error_experiencia'] = ['Los choferes deben tener almenos 5 años de experiencia contados desde la edad adulta.'] 
		"""

		#otros ...

	if object_type == 'Vehiculo':
		#Errores a puntualizar con relacion a los vehiculos.

		cantidad_asientos = request_data.get('cantidad_asientos')

		if cantidad_asientos:
			if cantidad_asientos > 150:#investigar ...
				errores['error_cantidad_asientos'] = ['ningún omnibus poseé mas de 150 asientos.']
		

		#Deberia permitirce que se cambien las placas?
		#otros ...

	if object_type == 'Viaje':
		
		#Para comporbar la validez de las fechas:
		#Deberia fijar un tiempo minimo para todos los viajes?
		inicio_viaje = request_data.get('inicio_viaje')#Estos son str que deben ser tansformdos a datetime objects.
		fin_viaje = request_data.get('fin_viaje')#Python puede hacer operaciones de comparacion (>, <, >=, <=, ==, !=) con strs que hace que esto sea funcional sin necesidad de usar datetime.  
		
		if inicio_viaje and fin_viaje:
		
			try:
				iv = dt.strptime(inicio_viaje, formato)
				fv = dt.strptime(fin_viaje, formato)		

				if iv >= fv:
					errores['error_fechas'] = ['La fecha de inicio del viaje debe ser mayor que la del fin de este.']	
 	
				else:
					#Si iv >= fv no tiene sentido calcular la duracion del viaje.
					#duracion = fv - iv
					duracion_dias_decimales = (fv - iv).total_seconds()/(24*60*60)
					if duracion_dias_decimales < (1/24):# 1/24 es el valor de una ura en dias.
						errores['error_fechas'] = ['Un viaje debe durar como munimo una hora, por favor revise las fechas de inicio y finalización del viaje.']
			
			except ValueError:
				errores['error_fechas'] = ['Las fechas deben ser ingresadas con el siguiente formato: %Y-%m-%dT%H:%M:%SZ']

		else:
			errores['error_fechas'] = ['Las campos de inicio y fin del viaje son obliagatorios.']
		
		#Para comporbar que se hayan asignado un chofer y un vehiculo validos:
		id_chofer = request_data.get('id_chofer')
		id_vehiculo = request_data.get('id_vehiculo')

		if id_chofer:
			chofer = do_query(Modelo = Chofer, ID = id_chofer)
			if not chofer:
				errores['error_chofer'] = ['No existe chofer con id = {} en la Base de Datos.'.format(id_chofer)]

			del chofer#Borrarlo ya que no será nesario en el resto de la ejecucion de la función.
		
		else:
			errores['error_chofer'] = ['Para poder crear o editar un viaje un chofer debe ser asiganado.']

		if id_vehiculo:
			vehiculo = do_query(Modelo = Vehiculo, ID = id_vehiculo)
			if not vehiculo:
				errores['error_vehiculo'] = ['No existe vehiculo con id = {} en la Base de Datos.'.format(id_vehiculo)]

			del vehiculo#Borrarlo ya que no será nesario en el resto de la ejecucion de la función.
		
		else:
			errores['error_vehiculo'] = ['Para poder crear o editar un viaje un vehiculo debe ser asiganado.']

		
		#Comprovar que esten los demas campos:

		tipo_viaje = request_data.get('tipo_viaje')
		#comentarios = request_data.get('comentarios')#No es obligatorio poner cometarios. 
		estado_viaje = request_data.get('estado_viaje')
		kms_recorridos = request_data.get('kms_recorridos')

		if not tipo_viaje:
			errores['error_tipo_viaje'] = ['Debe especificar el tipo de viaje.']

		if not estado_viaje:
			errores['error_estado_viaje'] = ['Debe especificar el estado del viaje.']	

		if not kms_recorridos:
			errores['error_kms_recorridos'] = ['Debe especificar cuantos kilometros seran recorridos en el viaje.']


		#otros errores con respecto a los viajes ...

	if object_type == 'SGVUser':
		password = request_data.get('password')

		if password:
			if len(password) < 8:
				errores['error_contasegna'] = ['La contraseña debe tener al menos 8 caracteres.']
		else:
			errores['error_contasegna'] = ['Debe asignar una contraseña.']


	return errores#Si no se cumple ninguna de las condiciones esto será {} = Flase.



def add_dicts(dict1, dict2):
	"""
	'Suma' dos diccionarios, es decir, toma las llaves y valores de dos diccionarios y los une en uno solo.	
	"""

	dict_resultante = {}

	for key, value in list(dict1.items()) + list(dict2.items()):
		dict_resultante[key] = value

	return dict_resultante	

"""
def add_data(request_data):

	#Agrega el chofer y el vehiculo al diccionario de la request para posteriomente ser agregado al serialzador.	  

	request_resultante = {}

	id_chofer = request_data.get('id_chofer')
	id_vehiculo = request_data.get('id_vehiculo')

	if id_chofer:
		chofer = do_query(Modelo = Chofer, ID = id_chofer)

	if id_vehiculo:
		vehiculo = do_query(Modelo = Vehiculo, ID = id_vehiculo)


	if id_vehiculo and id_chofer:
		if chofer and vehiculo:
			request_resultante['chofer'] = ChoferSerializer(chofer).data#El Chofer en formato JSON
			request_resultante['viaje'] = ViajeSerializer(viaje).data

			request_resultante = add_dicts(request_data, request_resultante)
			request_resultante.pop('id_chofer')
			request_resultante.pop('id_vehiculo')

			return request_resultante
		
	else:
		return request_data#Esto significa que, o no contenia los ids o no eran validos.
"""

def calcular_costo(viaje):
	"""
	#Calcula el costo (en dolares) de un viaje espesifico en funcion de su duracion, la catidad de asientos que posee el vehiculo que lo hizo y la cantidad de kilometros recorridos
	#agrega 500 dolares en caso de que el servicio sea de tipo VIP.		  
	"""

	iv = dt.strptime(viaje.inicio_viaje, formato)#ver linea No.06
	fv = dt.strptime(viaje.fin_viaje, formato)

	duracion = fv - iv#Esto es un objeto del tipo datetime.

	duracion = round(duracion.total_seconds()/(24*60*60), 3)

	costo = (duracion * viaje.vehiculo.cantidad_asientos * 0.21) + (1.2 * viaje.kms_recorridos)

	if viaje.vehiculo.tipo_servicio == "VIP":
		costo += 500

	costo = round(costo, 2)

	return costo







