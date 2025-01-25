from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Teacher(models.Model):
    #ФИО
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    parentName = models.CharField(max_length=50)
    #АЙДИ кафедры
    department_id = models.ForeignKey('Department', on_delete=models.PROTECT, null=False)

    def __str__(self):
        return f'{self.surname} {self.name} {self.parentName}' 

class Department(models.Model):
    name = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    teacher_id = models.ForeignKey('Teacher', on_delete=models.PROTECT, null=True, blank=True)
    department_id = models.ForeignKey('Department', on_delete=models.PROTECT, null=True, blank=True)

class Achivment_Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.name
    
class Achivment(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    # Айди категории достижения
    achivments_category_id = models.ForeignKey('Achivment_Category', on_delete=models.PROTECT, null=False)

class Teacher_Achivment(models.Model):
    teacher_id = models.ForeignKey('Teacher', on_delete=models.PROTECT, null=False)
    Achivment = models.ForeignKey('Achivment', on_delete=models.PROTECT, null=False)
    score = models.IntegerField(default=0)

class Score_Value(models.Model):
    Achivment = models.ForeignKey('Achivment', on_delete=models.PROTECT, null=False)
    score = models.IntegerField(default=0)