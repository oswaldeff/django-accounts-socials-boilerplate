from django.db import models

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models import base
from django.core.validators import RegexValidator
from django.db.models.fields import EmailField

# BaseUserManager & AbstractBaseUser django github url: https://github.com/django/django/blob/main/django/contrib/auth/base_user.py
# Usermanager django githun url: https://github.com/django/django/blob/main/django/contrib/auth/models.py

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
    
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
    
        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    User Model
    """
    objects = UserManager()
    
    user_pk = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=16, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=11, unique=True, blank=False, null=False, validators=[RegexValidator(r'^\d{3}-?[1-9]\d{3}-?\d{4}$')])
    email = EmailField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = '' # necessary
    REQUIRED_FIELDS = '' # not necessary
    
    class Meta:
        db_table = 'Users'
    
    def __str__(self):
        return str(self) # self.field