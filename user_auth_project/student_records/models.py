from django.db import models # type: ignore

class Admin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    # Role field (to handle role-switching)
    role = models.CharField(max_length=10, default="admin")  # Can be "admin" or "student"

    def __str__(self):
        return self.username


class Student(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    section = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username