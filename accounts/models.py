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
    
    
    def create_user(self, username, phone=None, email=None, password=None, **extra_fields):
        # if not password:
        #     raise ValueError('Password is Required')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, phone=None, email=None, password=None, **extra_fields):
        superuser = self.create_user(username=username, password=password, **extra_fields)
        superuser.set_password(password)
        superuser.is_superuser = True
        superuser.is_admin = True
        superuser.is_staff = True
        superuser.save(using=self._db)
        
        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    """
    User Model
    """
    objects = UserManager()
    
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=16, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=11, unique=True, blank=False, null=False, validators=[RegexValidator(r'^\d{3}-?[1-9]\d{3}-?\d{4}$')])
    email = EmailField(unique=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username' # necessary
    # REQUIRED_FIELDS = '' # not necessary
    
    class Meta:
        verbose_name_plural = '사용자 목록'
        db_table = 'users'
    
    def __str__(self):
        return self.id # self.field