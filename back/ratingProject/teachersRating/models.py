from django.db import models
from django.contrib.auth.models import AbstractUser



class Employee(models.Model):

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    parentName = models.CharField(max_length=50)
    email = models.CharField(max_length=500, null=True)
    department = models.ForeignKey('Department', on_delete=models.PROTECT, null=False)
    position = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f'{self.surname} {self.name} {self.parentName}' 

class Department(models.Model):

    name = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):

    employee = models.ForeignKey('Employee', on_delete=models.PROTECT, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.PROTECT, null=True, blank=True)
    role = models.CharField('role', max_length=50)

class Achievment_groups(models.Model):

    name = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.name    
    
class Achievment(models.Model):
    
    group = models.ForeignKey('Achievment_groups', null=True, on_delete=models.PROTECT,)
    parent_id = models.IntegerField(null=True)
    number = models.CharField(null=False, max_length=20)
    name = models.CharField(max_length=300, db_index=True)
    meas_unit = models.CharField(max_length=100)
    meas_unit_score = models.FloatField(default=0.0)
    # Информация о подтверждающем документе
    verif_doc_info = models.CharField(max_length=1000)

    def __str__(self):
        return self.number + " " + self.name

class Employee_Achievment(models.Model):

    employee = models.ForeignKey('Employee', on_delete=models.PROTECT, null=False)
    achievment = models.ForeignKey('Achievment', on_delete=models.PROTECT, null=False)
    full_achivment_name = models.CharField(max_length=300)
    meas_unit_val = models.CharField(max_length=50)
    score = models.FloatField(default=0.0)
    # Подтверждающий документ
    verif_doc = models.FileField(upload_to='verification_documents/', blank=True, null=True)  # Добавлено поле для файла
    verif_link = models.CharField(max_length=2000)
    reciving_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_achivment_name

    