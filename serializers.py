from gestion_vehiculos_api.models import Chofer, Vehiculo, Viaje#, GVUser
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

    #Si ejecuto este metdo antes de usar .save() optendré un AssertionError. 
	"""
	def validar_edad(self):
		return self.data['edad'] < 18
	"""

class VehiculoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vehiculo
        fields =	[	'id_vehiculo', 'placa', 'marca', 
        				'peso_en_toneladas', 'tipo_de_comnustible', 'kms_recorridos',
        				'velocidad_maxima', 'agnos_explotacion', 'tipo_servicio',
        				'climatizacion', 'cantidad_asientos', 'disponibilidad',
        			]
        
        #fields = '__all__'

class ViajeSerializer(serializers.HyperlinkedModelSerializer):
	
	chofer = ChoferSerializer()
	vehiculo = VehiculoSerializer()

	#print(chofer)


	class Meta:
		model = Viaje
		"""
		fields =	[	'id_viaje', 'tipo_viaje', 'inicio_viaje', 
						'fin_viaje', 'costo_usd', 'kms_recorridos',
						'comentarios', 'vehiculo', 'chofer',
						'estado_viaje',
					]
		"""	
		#fields = '__all__'

		fields =	['id_viaje', 'tipo_viaje', 'inicio_viaje', 'fin_viaje', 'costo_usd', 'kms_recorridos', 'comentarios', 'estado_viaje', 'chofer', 'vehiculo']

"""
class GVUserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = GVUser
		fields =	[	'nombre_completo', 'rol', 'cedula', 'edad', 
						'numero_telefono', 'direccion_particular',
						'email'
					]
"""































