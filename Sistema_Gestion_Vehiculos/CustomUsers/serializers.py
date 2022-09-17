from CustomUsers.models import SGVUser
from rest_framework import serializers


class SGVUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = SGVUser
		fields = [	'id', 'username', 'rol', 'email', 
					'nombre_completo', 'password']


	def create(self, validated_data):
		"""
		Cuando se ejecuta este metodo?
		Cuando se va a crear un nuevo user.
		"""

		password = validated_data.pop('password', None)#Borra la contaseña y la asigna a la variable.
		instancia = self.Meta.model(**validated_data)

		if password is not None:
			instancia.set_password(password)#Aqui se le aplicara el Algoritmo de encriptación.

		instancia.save()
		return instancia

	
	def update(self, instance, validated_data):
		"""
		Este metodo se ejecutara cunado se intente actualizar un SGVUser.
		"""		

		instance.username = validated_data.get('username', instance.username)#Intenta obtener la llave y si no lo hace toma la anterior.
		instance.rol = validated_data.get('rol', instance.rol)
		instance.email = validated_data.get('email', instance.email)
		instance.nombre_completo = validated_data.get('nombre_completo', instance.nombre_completo)	
		instance.password = validated_data.get('password', instance.password)

		if instance.password is not None:
			instance.set_password(instance.password)

		instance.save()
		return instance	




















