from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Child(models.Model):
    name = models.CharField(max_length=64)
    gender = models.CharField(max_length=5)
    birthday = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.gender}, {self.birthday}"


class Measurement(models.Model):
    weight = models.FloatField()
    height = models.FloatField()
    head_circumference = models.FloatField(blank=True)
    date = models.DateField(auto_now_add=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.child}, {self.weight}, {self.height}"
