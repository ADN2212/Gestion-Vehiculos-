from gestion_vehiculos_api.models import Chofer, Vehiculo, Viaje, GVUser
from rest_framework import serializers


"""
Esta parte define como que informacion de los modelo se mostrará en la respuesta (responce)
que dará la API cuando se le haga una peticion (request).  

"""

class ChoferSerializer(serializers.HyperlinkedModelSerializer):
	
	#edad = serializers.IntegerField()

	class Meta:
		model = Chofer
		fields =	['id_chofer', 'nombre_completo', 'edad', 'cedula',
        			'numero_telefono', 'direccion_particular', 'email',
        			'nivel_escolar', 'sexo', 'agnos_experiencia', 
        			'cantidad_de_multas', 'clasificacion']

	def validar_edad(self):
		return self.data['edad'] < 18





class VehiculoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'placa']

class ViajeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Viaje
		#fields = ['chofer', 'inicio_viaje', 'fin_viaje', 'costo_usd']
		fields = '__all__'

class GVUserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = GVUser
		fields =	[	'nombre_completo', 'rol', 'cedula', 'edad', 
						'numero_telefono', 'direccion_particular',
						'email'
					]





























