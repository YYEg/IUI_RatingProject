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
    # Флаги для отделения статейных
    is_pub = models.BooleanField(default=False)
    has_publication = models.BooleanField(default=False)
    has_conference = models.BooleanField(default=False)
    def __str__(self):
        return self.number + " " + self.name

class Pub_Grief(models.Model):
    name = models.CharField(max_length=50)
    has_levels = models.BooleanField(default=False)
    def __str__(self):
        return self.name 

class Pub_Level(models.Model):
    pub_grief = models.ForeignKey('Pub_Grief', on_delete=models.PROTECT, null=False)
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class Pub_Type(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Employee_Achievment(models.Model):
    #Общая информация
    employee = models.ForeignKey('Employee', on_delete=models.PROTECT, null=False)
    achievment = models.ForeignKey('Achievment', on_delete=models.PROTECT, null=False)
    meas_unit_val = models.CharField(max_length=50)
    score = models.FloatField(default=0.0)
    full_achivment_name = models.CharField(max_length=1000)
    # Подтверждающий документ
    verif_doc = models.FileField(upload_to='verification_documents/', blank=True, null=True)
    verif_link = models.CharField(max_length=2000, null=True)
    #Поля для статьи
    pub_type =  models.ForeignKey('Pub_Type', on_delete=models.PROTECT, null=True, blank=True)
    pub_grief = models.ForeignKey('Pub_Grief', on_delete=models.PROTECT, null=True, blank=True)
    pub_level = models.ForeignKey('Pub_Level', on_delete=models.PROTECT, null=True, blank=True)
    pub_language = models.CharField(max_length=50, null=True, blank=True)
    ru_full_name = models.CharField(max_length=1000, null=True, blank=True)
    pub_doi = models.CharField(max_length=200, null=True, blank=True)
    pub_authors_employees = models.CharField(max_length=1000, null=True, blank=True)
    pub_authors_students = models.CharField(max_length=1000, null=True, blank=True)
    pub_out_authors = models.CharField(max_length=1000, null=True, blank=True)
    bibliographic_desc = models.CharField(max_length=1000, null=True, blank=True)
    conference_name = models.CharField(max_length=200, null=True, blank=True)
    conference_status = models.CharField(max_length=50, null=True, blank=True)
    conference_date = models.DateField(null=True)
    publication_name = models.CharField(max_length=200, null=True, blank=True)
    publicator = models.CharField(max_length=200, null=True, blank=True)
    publication_data = models.DateField(null=True)
    publication_year_vol_num = models.CharField(max_length=200, null=True, blank=True)
    #Дополнительная общая информация
    reciving_date = models.DateField(null=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.full_achivment_name

    