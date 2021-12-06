from django.test import TestCase
from cryptodome import AESCipher
from django.http import JsonResponse

# Create your tests here.


def test_api(request):
    pass
    return JsonResponse({}, status=200)