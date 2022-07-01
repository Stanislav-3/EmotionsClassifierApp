import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
import logging


logger = logging.getLogger(__name__)


def get_upload_path(instance, filename):
    logger.debug('users.models get upload path')

    upload_to = 'users/images'

    ext = filename.split('.')[-1]
    filename = f'{instance.id}.{ext}'

    return os.path.join(upload_to, filename)


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to=get_upload_path)