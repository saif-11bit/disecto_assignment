from .models import User, WorkingPeriod
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import (
    ConsultantRegisterSerializer,
    VisitorRegisterSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
)
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
import jwt


class ConsultantRegisterView(generics.GenericAPIView):
    
    serializer_class = ConsultantRegisterSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data
        username = user_data['user'].get('username')
        
        user = User.objects.get(username=username)
        
        token = RefreshToken.for_user(user).access_token
        
        print("Token:", token)
        
        return Response(user_data,status=status.HTTP_201_CREATED)
    
    
class VisitorRegisterView(generics.GenericAPIView):
    
    serializer_class = VisitorRegisterSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data
        username = user_data['user'].get('username')
        
        user = User.objects.get(username=username)
        
        token = RefreshToken.for_user(user).access_token
        
        print("Token:", token)
        
        return Response(user_data,status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email':'Successfully activated'},status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation expired!'},status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid Token!'},status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):

        user = request.data
                
        serilaizer = self.serializer_class(data=user)
        serilaizer.is_valid(raise_exception=True)

        return Response(serilaizer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

class WorkingPeriodView(APIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        
        wp = WorkingPeriod.objects.filter(consultant_user_id=request.user.id).all()
        return Response(
            {
                'working periods': wp
            }
        )
