from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services.utils import *
from .services.services import *
from django.http import HttpRequest, HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("ok")

class Register(APIView):

    serializer_class: serializers.ModelSerializer = RegisterUserSerializer

    def post(self, request: HttpRequest):

        Register_services(request=request, serializer_class=self.serializer_class)
        
        return Response(status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get("token", None)

        if token is None:
            return Response({"error": "token is nullable"},status=status.HTTP_400_BAD_REQUEST)

        return VerifiEmail_services(token)


class AgainVerifyEmail(APIView):

    serializer_class: serializers.ModelSerializer = AgainVerifySerializer

    def post(self, request: HttpRequest):
        return AgainVerifyEmail_services(request=request, serializer_class=self.serializer_class)

class RegisterDevice(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class: serializers.ModelSerializer = RegisterDeviceSerializer

    def post(self, request: HttpRequest):
        return RegisterDevice_services(request=request, serializer_class=self.serializer_class)

    def delete(self, request: HttpRequest):
        return DeleteDevice_services(request=request, serializer_class=self.serializer_class)
