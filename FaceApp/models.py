import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager

# for creating unique directory for each USer 
def user_directory(instance,filename):
    print("_____________'user_{0}/{1}'.format(instance.uid,filename)_____________")
    return 'user_{0}/{1}'.format(instance.uid,filename)


class User(AbstractUser):
    username = None
    uid = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    email =models.EmailField(unique=True)
    image = models.FileField(upload_to='faces')

    USERNAME_FIELD = 'email'    #we want to login via email
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email