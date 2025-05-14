from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    parentName = models.CharField(max_length=50)
    email = models.CharField(max_length=500, null=True)
    department = models.ForeignKey('Department', on_delete=models.PROTECT, null=False)
    position = models.CharField(max_length=500, null=True)
    def __str__(self):
        return f'{self.surname} {self.name} {self.parentName}'

class User(AbstractUser):
    employee = models.ForeignKey('Employee', on_delete=models.PROTECT, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.PROTECT, null=True, blank=True)
    role = models.CharField('role', max_length=50)

class AchievmentGroup(models.Model):
    name = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=1000, null=True)
    def __str__(self):
        return self.name

class AchievmentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return self.name

class Achievment(models.Model):
    group = models.ForeignKey('AchievmentGroup', null=True, on_delete=models.PROTECT)
    parent_id = models.IntegerField(null=True)
    number = models.CharField(null=False, max_length=20)
    name = models.CharField(max_length=300, db_index=True)
    meas_unit = models.CharField(max_length=100)
    meas_unit_score = models.FloatField(default=0.0)
    verif_doc_info = models.CharField(max_length=1000)
    type = models.ForeignKey('AchievmentType', on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.number + " " + self.name

class EmployeeAchievment(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.PROTECT, null=False)
    achievment = models.ForeignKey('Achievment', on_delete=models.PROTECT, null=False)
    meas_unit_val = models.CharField(max_length=50)
    score = models.FloatField(default=0.0)
    full_achivment_name = models.CharField(max_length=1000)
    verif_doc = models.FileField(upload_to='verification_documents/', blank=True, null=True)
    verif_link = models.CharField(max_length=2000, null=True)
    reciving_date = models.DateField(null=True)
    active = models.BooleanField(default=True)
    details = models.JSONField(null=True, blank=True, verbose_name='Детали достижения')
    def __str__(self):
        return self.full_achivment_name

class PubGrief(models.Model):
    name = models.CharField(max_length=50)
    has_levels = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class PubLevel(models.Model):
    pub_grief = models.ForeignKey('PubGrief', on_delete=models.PROTECT, null=False)
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class PubType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

    