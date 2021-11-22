from django.http import JsonResponse
from .models import User
import os
import jwt
import datetime

def jwt_publish(platform, login_id):
    jwt_key = os.environ.get('JWT_KEY')
    jwt_expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*6)
    access_jwt = jwt.encode({'exp': jwt_expiration, 'login id': login_id}, key=jwt_key['SECRET KEY'], algorithm=jwt_key['ALGORITHM'])
    return access_jwt

def jwt_authorization(func):
    def wrapper(self, request, *args, **kwargs):
        jwt_key = os.environ.get('JWT_KEY')
        try:
            try:
                access_jwt = request.COOKIES.get('_utk')
            except:
                return JsonResponse({'message': 'GET JWT COOKIE ERROR'}, status=400)
            # decode
            payload = jwt.decode(access_jwt, key=jwt_key['SECRET KEY'], algorithms=jwt_key['ALGORITHM'])
            login_id = payload['login id']
            try:
                login_user = User.objects.get(id=login_id)
            except:
                return JsonResponse({'message': 'GET USER ERROR'}, status=400)
            
            request.user = login_user
            return func(self, request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'JWTOKEN EXPIRED'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'INVALID JWTOKEN'}, status=401)
    return wrapper