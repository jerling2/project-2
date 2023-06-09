"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from .views import index, schedulebuilder, professors, professor_data, courses, degreereqs


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('schedulebuilder/', schedulebuilder, name='schedulebuilder'),
    path('professors/', professors, name='professors'),
    path('professor-data/<str:professor>/', professor_data, name="professor_data"),
    path('courses/', courses, name='courses'),
    path('degreereqs/', degreereqs, name='degreereqs'),
] + static(settings.STATIC_URL)

