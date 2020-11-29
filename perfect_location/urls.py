"""perfect_location URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from location_module import views as location_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', location_views.home,name='home'),
    path('ajax/get_population_density/', location_views.get_population_density,name='get_population_density'),
    path('ajax/get_locations/', location_views.get_locations,name='get_locations'),
    path('ajax/get_address/', location_views.get_address,name='get_address'),
]
