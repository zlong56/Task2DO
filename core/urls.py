"""cswms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path , include 
from django.conf.urls.static import static
from django.conf import settings
from src import landing 

urlpatterns = [
    path('core/', admin.site.urls),
    path('', include('src.urls')),
    path('offline/', landing.offline, name='offline'),

    path('filePond_Upload_Handler/',landing.filePond_Upload_Handler, name='filePond_Upload_Handler'),
    path('clearTempFile/',landing.clearTempFile, name='clearTempFile'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path('manifest.json',landing.manifest_json_view)]
urlpatterns += [path('serviceworker.js',landing.serviceworker_view)]
urlpatterns += [path('favicon.ico',landing.favicon)]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    