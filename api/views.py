from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services.utils import *
from .services.services import *
from django.http import HttpRequest
from django.db.utils import IntegrityError
import jwt

# Create your views here.



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

        try:
            VerifiEmail_services(token)

            return Response({"status": "Email is Activated"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            return Response({"error": "Email is expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": "You have already used this link"}, status=status.HTTP_400_BAD_REQUEST)


class AgainVerifyEmail(APIView):

    serializer_class: serializers.ModelSerializer = AgainVerifySerializer

    def post(self, request: HttpRequest):
        return AgainVerifyEmail_services(request=request, serializer_class=self.serializer_class)
        
