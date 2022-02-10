from .models import User
from .serializers import UserSerializer
from core.exceptions import CustomKeyNotFoundAPIException
from django.contrib.auth.hashers import make_password, check_password
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
import re


# Create your views here.
def check_username_duplication(username):
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'INVALID USERNAME, ALREADY USED'}, status=400)
    
    return None

def check_phone_duplication(phone_number):
    
    if User.objects.filter(phone_number=phone_number).exists():
        return JsonResponse({'error': 'INVALID PHONE NUMBER, ALREADY USED'}, status=400)
    
    return None


def check_password_validation(password):
    
    if len(password)>int(16) or len(password)<int(8):
        return JsonResponse({'error': 'INVALID PASSWORD, PLEASE CHECK PASSWORD LENGTH'}, status=400)
    
    if re.search('[`~!@#$%^&*(),<.>/?]+', password) is None:
        return JsonResponse({'error': 'INVALID PASSWORD, PLEASE CHECK PASSWORD INCLUDES SPECIAL LETTER'}, status=400)
    
    if re.search('[0-9]', password) is None:
        return JsonResponse({'error': 'INVALID PASSWORD, PLEASE CHECK PASSWORD INCLUDES NUMBER'}, status=400)
    
    if re.search('[a-z]', password) is None:
        return JsonResponse({'error': 'INVALID PASSWORD, PLEASE CHECK PASSWORD INCLUDES SMALL LETTER'}, status=400)
    
    if re.search('[A-Z]', password) is None:
        return JsonResponse({'error': 'INVALID PASSWORD, PLEASE CHECK PASSWORD INCLUDES LARGE LETTER'}, status=400)
    
    return None


def check_phone_password_correct(username, password):
    
    if not User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'ACCOUNT NOT EXIST, PLEASE CHECK YOUR USERNAME'}, status=404)
    
    encoded = User.objects.get(username=username).password
    response = check_password(password, encoded, setter=None, preferred='default')
    
    if response is False:
        return JsonResponse({'error': 'PLEASE CHECK YOUR PASSWORD'}, status=404)
    
    return None


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
        
        response = check_username_duplication(username=username)
        if response:
            return response
        response = check_phone_duplication(phone_number=phone_number)
        if response:
            return response
        response = check_password_validation(password=password)
        if response:
            return response
        
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
        
        response = check_phone_password_correct(username, password)
        if response:
            return response
        
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