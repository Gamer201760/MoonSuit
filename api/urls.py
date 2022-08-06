"""abstactuser URL Configuration

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
from django.urls import include, path
from rest_framework.authtoken import views
from api.views import *
from .services.ObtainAuthToken import ObtainAuthToken


urlpatterns = [
    # path('getuserdata/', GetUserData.as_view()),
    path('login/', ObtainAuthToken.as_view()),
    # path('serialkey/create/', CreateSerialKey.as_view()),
    # path('serialkey/delete/<uuid:serialkey>/', CreateSerialKey.as_view()),
    path('register/', Register.as_view()),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("again-email-verify/", AgainVerifyEmail.as_view(), name="again-email-verify"),
    path('module/register/', RegisterDevice.as_view()),
    # path('module/delete/<pk>/', RegisterModule.as_view()),
    # path('module/register/<uuid:serialkey>/', RegisterModule.as_view()),
    # path('getmodulesinfo/', getModulesInfo.as_view()),
    # path('module/getinfo/<uuid:serialkey>/', getModuleInfo.as_view()),
    # path('getmodulename/<uuid:serialkey>/', getModuleName.as_view()),
]

