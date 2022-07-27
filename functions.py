from django.core.exceptions import ObjectDoesNotExist

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

	return errores#Si no se cumple ninguna de las condiciones esto será {} = Flase.



def add_dicts(dict1, dict2):
	"""
	'Suma' dos diccionarios, es decir, toma las llaves y valores de dos diccionarios y los une en uno solo.	
	"""

	dict_resultante = {}

	for key, value in list(dict1.items()) + list(dict2.items()):
		dict_resultante[key] = value

	return dict_resultante	





