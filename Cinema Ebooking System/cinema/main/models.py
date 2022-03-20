from django.db import models
from django.contrib.auth.models import User
# if you make changes here do this to apply them:
#python manage.py makemigrations main
#python manage.py migrate
#its like version control for git.
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(max_length=13)
    home_address = models.CharField(max_length=200)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    def __str__(self):
        return self.user.username

