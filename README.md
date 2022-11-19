Gestion-Vehiculos-API.

App que corresponde al BackEnd del proyecto, se extiende desde la Base de Datos hasta los Enpoints de la API.

Pasos a seguir para:

Cree un entorno virtual e instale las librerías que figuran en ‘requirements.txt’, luego de esto empiece un nuevo proyecto de Django llamado ‘Sistema_Gestion_Vehiculos’ dentro del cual deberá crear dos apps ‘CustomUsers’ y ‘gestion_vehiculos_api’, acto seguido sustituya las carpetas existentes por las que figuran en este repositorio.

Ademas de esto deberá tener instalado en su computador el gestor de bases de datos pgAdmin 4, ya que la App esta configurada para funcionar con Postgresql (ver settings.py, variable DATABASES) cree una base de datos cuyo nombre sea ‘GV_DB’ y contraseña ‘amaterasu’ o, en caso de querer otros valores cámbielos en la referencia antes dada.

Una vez haya completado estos pasos, usted estará en condiciones de poder correr la aplicación, ejecute las migraciones correspondientes y verifique en pgAmin 4 que las tablas de nombres Vehículo, Viaje, Chofer y SGVUser, están en la base de datos, luego cree un supeuser para poder acceder el panel de administración de Django, y con este cree un user de tipo admistrador para poder acceder a la app desde el FrontEnd.

Tome en cuenta que esta app es solo la mitad del proyecto, y que necesita ser complementada con el código que está en le repositorio ‘FrontEndApp-Let's Go Bus’.

