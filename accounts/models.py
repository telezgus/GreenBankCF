from django.db import models
from django.contrib.auth.models import User


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.IntegerField(
                            unique=True,
                            error_messages = {'unique':'DNI already exists'}
                            ) # recordar pasarlo a false una vez cargado el dni de los usuarios
    

    def __str__(self):
        return self.user.username