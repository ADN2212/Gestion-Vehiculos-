from django.db import models
#Estas dos permitiran crear un User Model personalizado.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class SGVUserManager(BaseUserManager):
	"""
	Esta clase definirá lo que va a pasar cuando un user o superUser es creado.
	hay que sobre-escribir los metodos para crear users y superusers.
	"""
	def create_user(self, nombre_completo, email, username, rol, password = None):

		#Estos errores no salen en el admin panel ni en las vistas de la API.
		if not email:
			raise ValueError('Todo usuario debe tener un email asignado.')

		if not nombre_completo:
			raise ValueError('Debe especificar el nombre completo del usuario.')

		if not username:
			raise ValueError('Debe agregar un nombre de usuario (username).')		

		if not rol:
			raise ValueError('Todo usuario debe tener un rol (Administrador, Agente o Supervisor).')

		if not password:
			raise ValueError('Debe agregar una contraseña.')

		if len(password) < 8:
			raise ValueError('La contraseña debe tener al menos 8 caracteres.')	

		#En caso de que no se cumpla ningua de estas excepciones:

		sgv_user = 	self.model(
					#pone el email en lowercase 
					email = self.normalize_email(email),
					username = username,
					rol = rol,
					nombre_completo = nombre_completo
			)

		sgv_user.set_password(password)
		sgv_user.save(using = self._db)
		return sgv_user

	def create_superuser(self, nombre_completo, username, password, email, rol):
		#Notece que se esta usando el metodo antes definido.
		user = self.create_user(
					nombre_completo = nombre_completo,
					email = self.normalize_email(email),
					password = password,
					username = username,
					rol = 'Administrador'
				)	

		#Como un super user puede hacerlo todo:
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True

		user.save(using = self._db)
		return user


class SGVUser(AbstractBaseUser):
	"""
	Clase que representara la tabla de usuarios en la BD del proyecto.
	"""
	#sobre escirbo la pk para tener una forma mas clara de referirme a esta.	
	#id_user = models.AutoField(primary_key = True)

	id = models.AutoField(primary_key = True)
	
	ROLES =	(
				('Administrador', 'Administrador'),
				('Agente', 'Agente'),
				('Supervisor', 'Supervisor')
			)

	rol = models.CharField(max_length = 13, choices = ROLES, verbose_name = 'Eliga el Rol de este Usuario')
	email = models.EmailField(verbose_name = 'Correo Electronico' , unique = True)
	username = models.CharField(max_length = 50, unique = True)
	nombre_completo = models.CharField(max_length = 100)

	#Los campos siguientes son obligatorios (required fields) para poder crear User Models personalizados:

	date_joined = models.DateTimeField(verbose_name = 'Fecha de Ingreso', auto_now_add = True)
	last_login = models.DateTimeField(verbose_name = 'Ultimo Ingreso', auto_now_add = True)
	is_admin = models.BooleanField(default = False)
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)

	#Esta variable define el campo con el que se hará login:
	USERNAME_FIELD = 'email'
	#Definir los campos oblgatorios:
	REQUIRED_FIELDS = ['rol', 'username', 'nombre_completo']

	#Espesificar el manager este modelo:
	objects = SGVUserManager()

	def __str__(self):
		return f'{self.nombre_completo}, {self.rol}'

	#Estos metodos son obligatorios:

	def has_perm(self, perm, obj = None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

	















