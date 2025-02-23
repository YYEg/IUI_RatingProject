from rest_framework import serializers
from .models import Employee, Department, Employee_Achievment, Achievment

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name', 'surname', 'parentName', 'department_id')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')


class AchievmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievment
        fields = ('id', 'name', 'meas_unit', 'meas_unit_score', 'verif_doc_info')

class Employee_AchievmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Achievment
        fields = '__all__'