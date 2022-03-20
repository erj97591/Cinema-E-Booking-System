from django.db import models
from django.contrib.auth.models import AbstractUser
# if you make changes here do this to apply them:
#python manage.py makemigrations main
#python manage.py migrate
#its like version control for git.
# Create your models here.
class custom_user(AbstractUser):
    phone_number = models.IntegerField()
    home_address = models.CharField(max_length=200)


