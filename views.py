#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from gestion_vehiculos_api.models import *
from django.views.decorators.csrf import csrf_exempt#Evita la proteccion a las CSRF. 
#from rest_framework.parsers import JSONParser
from gestion_vehiculos_api.serializers import * #Para poder mostrar la info.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from gestion_vehiculos_api.functions import * 




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
		
			choferes = do_query(Modelo = Chofer, order_by_arg = "-edad")

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
		
			vehiculos = do_query(Modelo = Vehiculo, order_by_arg = "peso_en_toneladas")

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

	#factory = APIRequestFactory()
	#requestx = factory.get('/get_viajes')

	#s_c = {'request': Request(requestx)}

	if request.method == 'GET':		
		
		if id == 'all':		
			viajes = do_query(Modelo = Viaje, order_by_arg = "-kms_recorridos")
			"""
			print('----------------------------------------------------')
			for v in viajes:
				print(v.chofer, v.vehiculo)
			print('----------------------------------------------------')
			"""
			if viajes:

				s_c = {'request': request}#El contexto es requerido cuando hay claves foraneas 

				return Response(ViajeSerializer(viajes, many = True, context = s_c).data)
				#return Response('Hola')

			return Response("No hay registros en la tabla de viajes", status = status.HTTP_404_NOT_FOUND)



















