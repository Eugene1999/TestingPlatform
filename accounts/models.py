from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    avatar = models.ImageField(location="users_avatars/")
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return "{} {} - {}".format(
            self.first_name,
            self.last_name,
            self.email
        )
