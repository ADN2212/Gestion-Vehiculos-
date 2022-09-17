from CustomUsers.models import SGVUser
from django.views.decorators.csrf import csrf_exempt 
from CustomUsers.serializers import SGVUserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from gestion_vehiculos_api.functions import do_query, add_errors, add_dicts
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def get_sgv_users(request, id):
	"""
	Endpoint de la API que sirve para hacer SELCT = GET a los SGVUsers. 
	"""

	if request.method == 'GET':

		if id == 'all':
			sgv_users = do_query(Modelo = SGVUser, order_by_arg = '-id')
			if sgv_users:
				return Response(SGVUserSerializer(sgv_users, many = True).data)

			return Response([])

		elif id.isdigit():
			sgv_user = do_query(SGVUser, ID = int(id))

			if sgv_user:
				return Response(SGVUserSerializer(sgv_user).data)

			return Response(f'No existe usuario de id = {id}')

		else:#En caso de que no se haga una request valida.
			return Response({ 'error': "opción no valida" }, status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
#Este decorador permitira que se acceda o no al view en funcion de los premisos que se pasen en la lista argumento.
#Para que una vista con 'IsAuthenticated' asignada se deberen enviar los tokens en los headers de la reques.
@permission_classes([IsAuthenticated])
def post_sgv_user(request):
	"""
	Endpoint de la API que sirve para hacer POST de un SGVUser, es decir, registrarce en la App.
	"""

	if request.method == 'POST':

		sgv_user_serializado = SGVUserSerializer(data = request.data) 

		errores = add_errors(request_data = request.data, object_type = 'SGVUser')

		if sgv_user_serializado.is_valid() and not errores:
			
			sgv_user_serializado.save()

			return Response('Usuario creado exitosamente', status = status.HTTP_201_CREATED)


		errores = add_dicts(errores, sgv_user_serializado.errors)

		return Response(errores, status = status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_sgv_user(request, id):
	"""
	Enpoint de la API que sirve para hacer DELETE de un USER espesifico.
	"""

	sgv_user = do_query(Modelo = SGVUser, ID = id)

	if request.method == 'GET':

		if sgv_user:
			return Response(SGVUserSerializer(sgv_user).data)

		return Response(f'No existe usuario con el id = {id} en la Base de Datos.', status = status.HTTP_404_NOT_FOUND)

	if request.method == 'DELETE':
		if sgv_user:
			sgv_user.delete()
			return Response(f'El usuario de id = {id} ha sido eliminado exitosamente.')

		return Response(f'No existe usuario con el id = {id} en la Base de Datos.', status = status.HTTP_404_NOT_FOUND)	


@api_view(['GET', 'PUT'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def put_sgv_user(request, id):
	"""
	Endpoint de la API que servirá para hacer PUT (actualizar) en un SGVUser.	 	
	"""

	sgv_user = do_query(Modelo = SGVUser, ID = id)

	if request.method == 'GET':
		if sgv_user:
			return Response(SGVUserSerializer(sgv_user).data)

		return Response(f'No existe usuario con el id = {id} en la Base de Datos.', status = status.HTTP_404_NOT_FOUND)

	if request.method == 'PUT':

		if sgv_user:

			errores = add_errors(request_data = request.data, object_type = 'SGVUser')
			sgv_user_serializado = SGVUserSerializer(sgv_user, data = request.data)

			if sgv_user_serializado.is_valid() and not errores:
				sgv_user_serializado.save()
				return Response(f'El user de id = {id} ha sido actualizado con exito')

			errores = add_dicts(errores, sgv_user_serializado.errors) 	
			return Response(errores, status = status.HTTP_400_BAD_REQUEST)

		return Response(f'No existe usuario con el id = {id} en la Base de Datos.', status = status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def blackListTokenView(request):
	
	"""
	Recibe el refresh token para enviarlo a la BlackLits
	"""

	if request.method == 'POST':
		try:
			rt = request.data['refresh']
			token = RefreshToken(rt)
			token.blacklist()
			return Response('El token ha sido cancelado con exito')

		except Exception:
			return Response('Error al cancelar el token', status = status.HTTP_400_BAD_REQUEST)

























