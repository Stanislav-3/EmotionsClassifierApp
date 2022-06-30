import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser


def get_upload_path(instance, filename):
    upload_to = 'users/images'

    ext = filename.split('.')[-1]
    filename = f'{instance.username}.{ext}'

    return os.path.join(upload_to, filename)


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to=get_upload_path)