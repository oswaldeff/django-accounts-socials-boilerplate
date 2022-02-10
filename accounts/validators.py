from .models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
import re


def username_duplication(username):
    
    if User.objects.filter(username=username).exists():
        raise ValidationError('INVALID USERNAME, ALREADY USED')

def phone_duplication(phone_number):
    
    if User.objects.filter(phone_number=phone_number).exists():
        raise ValidationError('INVALID PHONE NUMBER, ALREADY USED')


def password_validation(password):
    
    if len(password)>int(16) or len(password)<int(8):
        raise ValidationError('INVALID PASSWORD, PLEASE CHECK PASSWORD LENGTH')
    
    if re.search('[`~!@#$%^&*(),<.>/?]+', password) is None:
        raise ValidationError('INVALID PASSWORD, PLEASE CHECK PASSWORD INCLUDES SPECIAL LETTER')
    
    if re.search('[0-9]', password) is None:
        raise ValidationError('INVALID PASSWORD, PLEASE CHECK PASSWORD INCLUDES NUMBER')
    
    if re.search('[a-z]', password) is None:
        raise ValidationError('INVALID PASSWORD, PLEASE CHECK PASSWORD INCLUDES SMALL LETTER')
    
    if re.search('[A-Z]', password) is None:
        raise ValidationError('INVALID PASSWORD, PLEASE CHECK PASSWORD INCLUDES LARGE LETTER')


def phone_password_correction(username, password):
    
    if not User.objects.filter(username=username).exists():
        raise ValidationError('ACCOUNT NOT EXIST, PLEASE CHECK YOUR USERNAME')
    
    encoded = User.objects.get(username=username).password
    response = check_password(password, encoded, setter=None, preferred='default')
    
    if response is False:
        raise ValidationError('PLEASE CHECK YOUR PASSWORD')