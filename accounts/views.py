from .models import User
from .validators import username_duplication, phone_duplication, password_validation, phone_password_correction
from core.exceptions import CustomKeyNotFoundAPIException
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenViewBase, TokenObtainPairView
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.


class UserSignUpView(TokenObtainPairView, TokenViewBase):
    '''
        sign up
        
        ---
        ### Body Data
        - name: string
        ---
        ### Password Validation
        - must be over 8 and under 16 letters
        - must include special letter and number, small letter, large letter
        ---
    '''
    
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer
    
    www_authenticate_realm = 'api'
    
    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(AUTH_HEADER_TYPES[0], self.www_authenticate_realm)
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        
        try:
            username = request.data['username']
            phone_number = request.data['phone_number']
            password = request.data['password']
        except:
            return CustomKeyNotFoundAPIException()
        
        username_duplication(username=username)
        phone_duplication(phone_number=phone_number)
        password_validation(password=password)
        
        password = make_password(password=password, salt=None, hasher='default')
        user_object = User.objects.create(username=username, password=password)
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        response = {}
        response['message'] = 'SUCCESSFULLY SIGNED UP'
        response['account'] = User.objects.filter(id=str(user_object)).values('id', 'username', 'created')[0]
        response['token'] = serializer.validated_data
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, status=status.HTTP_201_CREATED)


class UserSignInView(TokenObtainPairView, TokenViewBase):
    '''
        sign in
        
        ---
        ### Body Data
        - phone: string
        - password: string
        ---
    '''
    
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer
    
    www_authenticate_realm = 'api'
    
    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(AUTH_HEADER_TYPES[0], self.www_authenticate_realm)
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            return CustomKeyNotFoundAPIException()
        
        phone_password_correction(username, password)
        
        user_object = User.objects.get(username=username)
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        response = {}
        response['message'] = 'SUCCESSFULLY SIGNED IN'
        response['account'] = User.objects.filter(id=str(user_object)).values('id', 'username', 'created')[0]
        response['token'] = serializer.validated_data
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, status=status.HTTP_200_OK)


class TokenRefreshView(TokenViewBase):
    '''
        token refresh
        
        ---
        ### Body Data
        - refresh: string
        ---
    '''
    
    permission_classes = [AllowAny]
    serializer_class = serializer_class = TokenRefreshSerializer
    
    www_authenticate_realm = 'api'
    
    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(AUTH_HEADER_TYPES[0], self.www_authenticate_realm)
    
    @csrf_exempt
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer refresh token", type=openapi.TYPE_STRING)])
    def post(self, request, *args, **kwargs):
        
        try:
            refresh = request.data['refresh']
        except:
            return CustomKeyNotFoundAPIException()
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        response = {}
        response['message'] = 'SUCCESSFULLY TOKEN REFRESHED'
        response['token'] = serializer.validated_data
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, status=status.HTTP_200_OK)