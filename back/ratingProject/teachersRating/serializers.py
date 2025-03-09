from rest_framework import serializers
from .models import Employee, Department, Employee_Achievment, Achievment, Pub_Grief, Pub_Level, Pub_Type

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
        fields = '__all__'

class Employee_AchievmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Achievment
        fields = '__all__'

class PubTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pub_Type
        fields = '__all__'

class PubGriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pub_Grief
        fields = '__all__'

class PubLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pub_Level
        fields = '__all__'