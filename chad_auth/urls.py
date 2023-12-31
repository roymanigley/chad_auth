"""
URL configuration for chad_auth project.

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from chad_auth import settings
from chad_auth_api.views import api
from chad_auth_oidc.views import api as oidc_api

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('oidc/', oidc_api.urls),
    path('login', TemplateView.as_view(template_name='login.html')),
    path('', TemplateView.as_view(template_name='home.html'))
])
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)