#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from gestion_vehiculos_api.models import *
from django.views.decorators.csrf import csrf_exempt#Evita la proteccion a las CSRF. 
#from rest_framework.parsers import JSONParser
from gestion_vehiculos_api.serializers import * #Para poder mostrar la info.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

#Crear un EndPoint de la API usando una funcion como vista.
@api_view(['GET'])
@csrf_exempt
def  get_choferes(request, id):
	"""
	Enpoint de la API que sirve para hacer SLECT = GET, de uno o varios choferes.
	"""
	if request.method == 'GET':

		if id == 'all':

			print(request.path)

			#Hacer la query:
			choferes = Chofer.objects.all().order_by('-edad')

			#Serializar los objestos del modelo para que pueden ser transformados a JSONs:
			choferes_serializados = ChoferSerializer(choferes, many = True)

			#transformar a JSONS:
			choferes_JSONs = Response(choferes_serializados.data)

			return choferes_JSONs

		elif id.isdigit():#En caso de que sea un digito selecioar el objeto espesifico al que corresponde este id.  
			try:
				chofer = Chofer.objects.get(id_chofer = int(id))
				return  Response(ChoferSerializer(chofer).data) 
			
			except ObjectDoesNotExist:
				return Response( {'error': 'No existe coher con id = {}'.format(id)} )
		
		else:#En caso de que no se haga una request valida.
			return Response(status = status.HTTP_400_BAD_REQUEST)

	


@api_view(['POST'])
@csrf_exempt
def post_chofer(request):
	"""
	Endpoint de la API que sirve para ingresar datos en la Base de Datos, es decir, hacer INSERT = PSOT	 
	"""
	if request.method == 'POST':
		#print(request.path, '----------------')

		post_data = request.data#Esto es un diccionario de python

		chofer_serializado = ChoferSerializer(data = post_data)


		def add_errors(chz):
			"""
			Prueba si hay errores espesifcos dentro del chofer serilizado,
			y los agrega en caso de.
			"""
			errores = {}
			
			if chz.validar_edad():
				errores['edad'] = 'El chofer debe ser mayor de edad.'
			
			# ... demas pruebas.

			return errores#Si no se cumple ninguna de las condiciones esto sera {} = Flase.

		if chofer_serializado.is_valid():

			errores = add_errors(chofer_serializado)

			if errores:
				return Response(errores, status = status.HTTP_400_BAD_REQUEST)

			return Response(data_serializada.data)#Aqui tendria que guardar la info usando save().
		
		errores = chofer_serializado.errors#Lo copio por que no se puede editar el original.
		
		#Agregar los demas errores
		for error, descripcion in add_errors(chofer_serializado).items():
			errores[error] = descripcion 

		return Response(errores, status = status.HTTP_400_BAD_REQUEST)

















