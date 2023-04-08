from django.db import models


class Student(models.Model):

    name = models.TextField(max_length=10)

    birth_date = models.DateField(
        null=True,
    )

    def __str__(self):
       return f'{self.name}, {self.birth_date}'

class Course(models.Model):

    name = models.TextField(max_length=10)

    students = models.ManyToManyField(
        Student,
        blank=True,
    )