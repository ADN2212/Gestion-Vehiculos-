from gestion_vehiculos_api.models import Chofer, Vehiculo, Viaje
from rest_framework import serializers

"""
Esta parte define que informacion de los modelos se mostrará en la respuesta (responce)
que dará la API cuando se le haga una peticion (request).  

"""

class ChoferSerializer(serializers.HyperlinkedModelSerializer):
	
	#edad = serializers.IntegerField()

	class Meta:
		model = Chofer
		fields =	['id_chofer', 'nombre_completo', 'edad', 'cedula',
        			'numero_telefono', 'direccion_particular', 'email',
        			'nivel_escolar', 'sexo', 'agnos_experiencia', 
        			'cantidad_de_multas', 'clasificacion', 'cantidad_viajes']

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
        				'climatizacion', 'cantidad_asientos', 'disponibilidad', 'cantidad_viajes'
        			]
        
        #fields = '__all__'

class ViajeSerializer(serializers.HyperlinkedModelSerializer):
	
	chofer = ChoferSerializer()
	vehiculo = VehiculoSerializer()

	class Meta:
		model = Viaje
		fields =	[	
						'id_viaje', 'tipo_viaje', 'inicio_viaje', 
						'fin_viaje', 'costo_usd', 'kms_recorridos', 
						'comentarios', 'estado_viaje', 'chofer', 
						'vehiculo'
					]




























