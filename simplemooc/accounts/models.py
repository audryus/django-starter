import re

from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
    UserManager)
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(
    'User Name', max_length=30, unique=True, 
    validators=[validators.RegexValidator(re.compile(r'^[\w.@+-]+$'),
      'User name can only have letters, numbers or '
      'the following: @/./+/-/_', 'invalid')]
  )
  email = models.EmailField('E-mail', unique=True)
  name = models.CharField('Name', max_length=100, blank=True)
  is_active = models.BooleanField('Active?', blank=True, default=True)
  is_staff = models.BooleanField('Staff?', blank=True, default=False)
  date_joined = models.DateTimeField('Join date', auto_now_add=True)

  objects = UserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  def __str__(self):
      return self.name or self.username

  def get_short_name(self):
      return self.username

  def get_full_name(self):
      return str(self)

  class Meta:
      verbose_name = 'User'
      verbose_name_plural = 'Users'

class PasswordReset(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,
    on_delete=models.DO_NOTHING,
    verbose_name='User',
    related_name='resets'
  )
  key = models.CharField('Key', max_length=100, unique=True)
  created_at = models.DateTimeField('Created at', auto_now_add=True)
  confirmed = models.BooleanField('Confirmed?', default=False, blank=True)

  def __str__(self):
      return '{0} at {1}'.format(self.user, self.created_at)

  class Meta:
      verbose_name = 'New Password'
      verbose_name_plural = 'New Passwords'
      ordering = ['-created_at']