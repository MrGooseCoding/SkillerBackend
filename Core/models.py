from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username