#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from gestion_vehiculos_api.models import *
from django.views.decorators.csrf import csrf_exempt#Evita la protección a las CSRF. 
#from rest_framework.parsers import JSONParser
from gestion_vehiculos_api.serializers import * #Para poder mostrar la info.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.request import Request
#from rest_framework.test import APIRequestFactory
from gestion_vehiculos_api.functions import do_query, add_errors, add_dicts, calcular_costo 

#-------------------------------------------------------------------------EndPoint Que Muestra el Menú de la API-------------------------------------------------------------------------

@api_view(['GET'])
@csrf_exempt
def api_menu(request):
	"""
	Envia un JSON con informacion sobre las funcionalidades de la API.
	"""
	if request.method == 'GET':
		
		api_info = {
		
		'Lista de Opciones' : 'Ver siguientes...',
		'get_choferes/<str:id>' : 'Retorna el chofer con el id espesificado, o todos si se agrega "all" como argumento.',
    	'post_chofer' : 'Permite agregar un nuevo chofer',
    	'put_chofer/<int:id>': 'Permite actualizar el chofer al que pertenece el id que se pasa como argumento.',
    	'delete_chofer/<int:id>' : 'Permite borrar el chofer al que pertenece el id que se pasa como argumento.',
 		'hr' : '--------------------------------------------------------------------------------------------------------',
		'get_vehiculos/<str:id>' : 'Retorna el vehiculo con el id espesificado, o todos si se agrega "all" como argumento.',
    	'post_vehiculo' : 'Permite agregar un nuevo vehiculo',
    	'put_vehiculo/<int:id>': 'Permite actualizar el vehiculo al que pertenece el id que se pasa como argumento.',
    	'delete_vehiculo/<int:id>' : 'Permite borrar el vehiculo al que pertenece el id que se pasa como argumento.',    	 
    	'hr2' : '--------------------------------------------------------------------------------------------------------',
		'get_viajes/<str:id>' : 'Retorna el viaje con el id espesificado, o todos si se agrega "all" como argumento.',
    	'post_viaje' : 'Permite agregar un nuevo viaje',
    	'put_viaje/<int:id>': 'Permite actualizar el viaje al que pertenece el id que se pasa como argumento.',
    	'delete_viaje/<int:id>' : 'Permite borrar el viaje al que pertenece el id que se pasa como argumento.',
    	
    	}
		
		return Response(api_info)


#---------------------------------------------------------------------EndPoints Chofer----------------------------------------------------------------------------------------------------

#Crear un EndPoint de la API usando una funcion como vista.
@api_view(['GET'])
@csrf_exempt
def  get_choferes(request, id):
	"""
	Enpoint de la API que sirve para hacer SLECT = GET, de uno o varios choferes.
	"""
	if request.method == 'GET':

		if id == 'all':
		
			choferes = do_query(Modelo = Chofer, order_by_arg = "-id_chofer")

			if choferes:
				return Response(ChoferSerializer(choferes, many = True).data)

			return Response("No hay registros en la tabla de choferes", status = status.HTTP_404_NOT_FOUND)


		elif id.isdigit():#En caso de que sea un digito selecioar el objeto espesifico al que corresponde este id.  
						
			chofer = do_query(Chofer, ID = int(id))

			if chofer:
				return Response(ChoferSerializer(chofer).data)


			return Response( {'error': 'No existe chofer con id = {}'.format(id)}, status = status.HTTP_404_NOT_FOUND)			

		else:#En caso de que no se haga una request valida.
			return Response({ 'error': "opción no valida" }, status = status.HTTP_400_BAD_REQUEST)

	


@api_view(['POST'])
@csrf_exempt
def post_chofer(request):
	"""
	Endpoint de la API que sirve para ingresar datos en la Base de Datos, es decir, hacer INSERT = PSOT	 
	"""
	if request.method == 'POST':
		#print(request.path, '----------------')

		post_data = request.data#Esto es un diccionario de python

		errores = add_errors(request_data = post_data, object_type = 'Chofer')

		chofer_serializado = ChoferSerializer(data = post_data)

		if chofer_serializado.is_valid() and not errores:

			chofer_serializado.save()

			return Response('Chofer creado exitosamente', status = status.HTTP_201_CREATED)#Aqui tendria que guardar la info usando save().
		
		errores = add_dicts(errores, chofer_serializado.errors)
		
		return Response(errores, status = status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'GET'])
@csrf_exempt
def put_chofer(request, id):
	
	"""
	Endpoint de la API que servirá para actualizar (PUT = UPDATE) un chofer. 
	"""
	
	chofer = do_query(Modelo = Chofer, ID = id)

	if request.method == 'GET':
		
		if chofer:
			return Response(ChoferSerializer(chofer).data)

		return Response({'error': 'No existe chofer con id = {}'.format(id)}, status = status.HTTP_404_NOT_FOUND)#Si la informacion que llega no está en formato JSON esta linea retornara un JSON con el mensaje de que el formato no es correcto.

	if request.method == 'PUT':


		if chofer:

			errores = add_errors(request_data = request.data, object_type = 'Chofer')

			chofer_serializado = ChoferSerializer(chofer, data = request.data)
			
			if chofer_serializado.is_valid() and not errores:
				chofer_serializado.save()
							
				return Response('Chofer actualizdo exitosamente')#, status = status.HTTP_205_RESET_CONTENT)

			errores = add_dicts(errores, chofer_serializado.errors)
		
			return Response(errores, status = status.HTTP_400_BAD_REQUEST)

		return Response({'error': 'No existe chofer con id = {}'.format(id)}, status = status.HTTP_404_NOT_FOUND)#Si la informacion que llega no está en formato JSON esta linea retornara un JSON con el mensaje de que el formato no es correcto.

	"""
	if request.method == 'POST':

		return HttpResponse('Hola')
	"""

@api_view(['GET', 'DELETE'])
@csrf_exempt
def delete_chofer(request, id):
	
	"""
	Endpoint de la API que servirá para borrar (DELETE = DELETE) un chofer. 
	"""
	
	chofer = do_query(Modelo = Chofer, ID = id)

	if request.method == 'GET':

		return Response(ChoferSerializer(chofer).data) if chofer else Response({'error': 'No existe chofer con id = {}'.format(id)}, status = status.HTTP_404_NOT_FOUND)

	if request.method == 'DELETE':
		
		if chofer:
			chofer.delete()
			return Response('{} ha sido borrado de la plantilla de choferes'.format(chofer.nombre_completo))

		return Response('No se puede borrar un chofer que no existe', status = status.HTTP_400_BAD_REQUEST)
			

#------------------------------------------------------------------Enpoints para Vehiculos-------------------------------------------------------------------------------

@api_view(['GET'])
@csrf_exempt
def  get_vehiculos(request, id):
	"""
	Enpoint de la API que sirve para hacer SLECT = GET, de uno o varios vehiculos.
	"""
	if request.method == 'GET':

		if id == 'all':
		
			vehiculos = do_query(Modelo = Vehiculo, order_by_arg = "-id_vehiculo");

			if vehiculos:
				return Response(VehiculoSerializer(vehiculos, many = True).data)

			return Response("No hay registros en la tabla de vehiculos", status = status.HTTP_404_NOT_FOUND)


		elif id.isdigit():  
						
			vehiculo = do_query(Modelo = Vehiculo, ID = int(id))

			if vehiculo:
				return Response(VehiculoSerializer(vehiculo).data)


			return Response( {'error': 'No existe omnibus con id = {}'.format(id)}, status = status.HTTP_404_NOT_FOUND)			

		else:#En caso de que no se haga una request valida.
			return Response({ 'error': "opción no valida" }, status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def post_vehiculo(request):
	"""
	Endpoint de la API que sirve para ingresar datos en la tabla vehiculos, es decir, hacer INSERT = POST	 
	"""
	if request.method == 'POST':

		errores = add_errors(request_data = request.data, object_type = 'Vehiculo')

		vehiculo_serializado = VehiculoSerializer(data = request.data)

		if vehiculo_serializado.is_valid() and not errores:

			vehiculo_serializado.save()

			return Response('Vehiculo creado exitosamente', status = status.HTTP_201_CREATED)#Aqui tendria que guardar la info usando save().
		
		errores = add_dicts(errores, vehiculo_serializado.errors)
		
		return Response(errores, status = status.HTTP_400_BAD_REQUEST)




@api_view(['PUT', 'GET'])
@csrf_exempt
def put_vehiculo(request, id):
	"""
	Endponit de la API que sirve para hacer PUT = UPDATE a los vehiculos de la BD. 
	"""
	vehiculo = do_query(Modelo = Vehiculo, ID = id)

	if request.method == 'GET':
		return Response(VehiculoSerializer(vehiculo).data) if vehiculo else Response({'error': 'No existe vehiculo con id = {}'.format(id)}, status = status.HTTP_404_NOT_FOUND)

	
	if request.method == 'PUT':

		if vehiculo:

			errores = add_errors(request_data = request.data, object_type = 'Vehiculo')

			vehiculo_serializado = VehiculoSerializer(vehiculo, data = request.data)

			if vehiculo_serializado.is_valid() and not errores:

				vehiculo_serializado.save()

				return Response('El vehiculo de id = {} placa = {} ha sido actualizado'.format(id, request.data.get('placa')))

			errores = add_dicts(errores, vehiculo_serializado.errors)

			return Response(errores, status = status.HTTP_400_BAD_REQUEST)

		return Response('No hemos podido hallar este vehiculo')	


@api_view(['GET', 'DELETE'])
@csrf_exempt
def delete_vehiculo(request, id):
	
	"""
	Endpoint de la API que servirá para borrar (DELETE = DELETE) un vehiculo. 
	"""
	
	vehiculo = do_query(Modelo = Vehiculo, ID = id)

	if request.method == 'GET':

		return Response(VehiculoSerializer(vehiculo).data) if vehiculo else Response({'error': 'No existe vehiculo con id = {}'.format(id)}, status = status.HTTP_404_NOT_FOUND)

	if request.method == 'DELETE':
		
		if vehiculo:
			vehiculo.delete()
			return Response('El omnibus de marca = {}, placa = {} e id = {} a sido eliminado'.format(vehiculo.marca, vehiculo.placa, id))

		return Response('No se puede borrar un omnibus que no existe', status = status.HTTP_400_BAD_REQUEST)


#----------------------------------------------------------------Endpoints para Viajes-------------------------------------------------------------------------------------------			

@api_view(['GET'])
@csrf_exempt
def get_viajes(request, id):
	"""
	Enpoint de la API que sirve para hacer SELECT = GET, de uno o varios viajes.
	"""

	if request.method == 'GET':		
		
		s_c = {'request': request}

		if id == 'all':		
			viajes = do_query(Modelo = Viaje, order_by_arg = "-id_viaje")#Order_by_arg, tambien puede ser resivido en la URL como argumento
						
			if viajes:
				"""
				Si hago esto aqui estaré malgastondo potencia de computo.
				#Actualizar el costo de cada viaje:
					for v in viajes:
						v.calcular_costo()
				"""
				s_c = {'request': request}#El contexto es requerido cuando hay claves foraneas 

				return Response(ViajeSerializer(viajes, many = True, context = s_c).data)
				#return Response('Hola')

			return Response("No hay registros en la tabla de viajes", status = status.HTTP_404_NOT_FOUND)


		if id.isdigit():

			viaje = do_query(Modelo = Viaje, ID = int(id))

			if viaje:
				return Response(ViajeSerializer(viaje).data)#El context no es nesesario para un unico viaje?

			return Response( {'error' : 'No hay ningun viaje con id = {}'.format(id)} )	


@api_view(['POST'])
@csrf_exempt
def post_viaje(request):
	"""
	Endpoint de la API que sirve para ingresar datos en la tabla viajes de la BD, es decir, hacer INSERT = POST.
	El JSON de la request debe contener los ids del chofer y el vehiculo.	 
	"""
	if request.method == 'POST':

		post_data = request.data#Esto es un diccionario de python

		errores = add_errors(request_data = post_data, object_type = 'Viaje')

		#print(post_data)

		viaje_serializado = ViajeSerializer(data = post_data, partial = True)#'partial' permite que el el serializer se haga con un JSON incompleto.

		#partial = True
		#print(viaje_serializado);

		if viaje_serializado.is_valid() and not errores:

			#viaje_serializado.save()

			#llagados a este punto ninguna de estas dos debería retorna None
			chofer = do_query(Modelo = Chofer, ID = request.data['chofer']['id_chofer'])
			vehiculo = do_query(Modelo = Vehiculo, ID = request.data['vehiculo']['id_vehiculo'])

			viaje =	Viaje(
							tipo_viaje = request.data['tipo_viaje'],
							inicio_viaje = request.data['inicio_viaje'],
							fin_viaje = request.data['fin_viaje'],
							costo_usd = 0,				
							kms_recorridos = request.data['kms_recorridos'],
							comentarios = request.data['comentarios'],
							estado_viaje = request.data['estado_viaje'],
							chofer = chofer,
							vehiculo = vehiculo
						)
		
			viaje.costo_usd = calcular_costo(viaje)

			viaje.save()

			return Response('El viaje fue creado exitosamente', status = status.HTTP_201_CREATED)
		
		errores = add_dicts(errores, viaje_serializado.errors)
		
		return Response(errores, status = status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'GET'])
@csrf_exempt
def put_viaje(request, id):
	"""
	Endponit de la API que sirve para hacer PUT = UPDATE a los viajes de la BD. 
	El JSON de la request debe contener los ids del chofer y el vehiculo.
	"""
	viaje = do_query(Modelo = Viaje, ID = id)

	if request.method == 'GET':

		
		if viaje:
		#Para mostrar solo los ids del chofer y el vehiculo correspondientes al viaje. 
			response = ViajeSerializer(viaje).data
			response['id_chofer'] = response['chofer']['id_chofer'] if response.get('chofer') else None #En caso de que le chofer o el vaje hayan sido borrados.
			response['id_vehiculo'] = response['vehiculo']['id_vehiculo'] if response.get('vehiculo') else None# el None de Python es null en JS.
		#En este caso no estoy interesado en todos los datos del chofer y el vehiculo:
			response.pop('chofer')
			response.pop('vehiculo')
		#Tampoco es nesesario mostrar el id:
			response.pop("id_viaje")	

			return Response(response)

		else:
			return Response({'error': 'No existe viaje con id = {}'.format(id)}, status = status.HTTP_404_NOT_FOUND)

		#return Response(ViajeSerializer(viaje).data) if viaje else Response({'error': 'No existe viaje con id = {}'.format(id)}, status = status.HTTP_404_NOT_FOUND)

	
	if request.method == 'PUT':
		

		if viaje:
			viaje_serializado = ViajeSerializer(viaje, data = request.data, partial = True)
			errores = add_errors(request_data = request.data, object_type = 'Viaje')

			if viaje_serializado.is_valid() and not errores:

				#Asignar los valores actualizados al registro.
				viaje.tipo_viaje = request.data['tipo_viaje']
				viaje.inicio_viaje = request.data['inicio_viaje']				
				viaje.fin_viaje = request.data['fin_viaje']
				viaje.kms_recorridos = request.data['kms_recorridos']
				viaje.comentarios = request.data.get('comentarios') if request.data.get('comentarios') else "..."
				viaje.estado_viaje = request.data['estado_viaje']
				viaje.chofer = do_query(Modelo = Chofer, ID = request.data['id_chofer'])
				viaje.vehiculo = do_query(Modelo = Vehiculo, ID = request.data['id_vehiculo'])
				#Luego de que los campos sean actualizados se puede re-caulcular el costo del vaije.
				viaje.costo_usd = calcular_costo(viaje)#Actualizar el costo del viaje.

				viaje.save()

				return Response('El viaje de id = {}  ha sido actualizado exitosamente'.format(id))

		#return Response(" Wait a ")

			else:
				errores = add_dicts(errores, viaje_serializado.errors)
				return Response(errores, status = status.HTTP_400_BAD_REQUEST)

		else:
			return Response({'error': 'No existe viaje con id = {}'.format(id)}, status = status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'DELETE'])
@csrf_exempt
def delete_viaje(request, id):
	
	"""
	Endpoint de la API que servirá para borrar (DELETE = DELETE) un viaje. 
	"""
	
	viaje = do_query(Modelo = Viaje, ID = id)

	if request.method == 'GET':

		return Response(ViajeSerializer(viaje).data) if viaje else Response({'error': 'No existe viaje con id = {} en esta Base de Datos'.format(id)}, status = status.HTTP_404_NOT_FOUND)

	if request.method == 'DELETE':
		
		if viaje:
			viaje.delete()
			return Response('El viaje de id = {} y tipo {} ha sido eliminado exitosamente'.format(id, viaje.tipo_viaje))

		return Response('No se ha encontado viaje con id = {}'.format(id), status = status.HTTP_404_NOT_FOUND)













