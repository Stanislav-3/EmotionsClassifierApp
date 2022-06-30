import os
from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import CustomUser


def get_upload_path(instance, filename):
    upload_to = f'computations/images/{instance.user.id}'

    ext = filename.split('.')[-1]
    filename = f'{instance.id}.{ext}'

    return os.path.join(upload_to, filename)


class Computation(models.Model):
    predictions = ArrayField(models.FloatField(), size=7)
    image = models.ImageField(upload_to=get_upload_path)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} | {self.image}'
