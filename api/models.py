from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    username_validator = AbstractUser.username_validator
    username = models.CharField(
        ('username'),
        max_length=32,
        unique=True,
        help_text=('Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
        primary_key=True
    )
    email = models.EmailField(('email address'), blank=False, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username