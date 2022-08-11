"""Sistema_Gestion_Vehiculos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#---------------------Para la Rest API----------------------------------
from gestion_vehiculos_api.views import * #Importa todas las vistas disponibles.


#--------------------------------URLs--------------------------------------

urlpatterns = [

    path('admin/', admin.site.urls),  
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    
    #URLs para choferes:
    path('get_choferes/<str:id>', get_choferes),
    path('post_chofer', post_chofer),
    path('put_chofer/<int:id>', put_chofer),
    path('delete_chofer/<int:id>', delete_chofer),
    
    #URLs para vehiculos:
    path('get_vehiculos/<str:id>', get_vehiculos),
    path('post_vehiculo', post_vehiculo),
    path('put_vehiculo/<int:id>', put_vehiculo),
    path('delete_vehiculo/<int:id>', delete_vehiculo),

    #URLs para viajes:
    path('get_viajes/<str:id>', get_viajes),
    path('post_viaje', post_viaje),
    path('put_viaje/<int:id>', put_viaje),
    path('delete_viaje/<int:id>', delete_viaje),

    #URLs para los usuarios:

]






