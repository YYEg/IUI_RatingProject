from rest_framework import serializers
from .models import Employee, Department, EmployeeAchievment, Achievment, PubGrief, PubLevel, PubType

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

class EmployeeAchievmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAchievment
        fields = '__all__'

class PubTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PubType
        fields = '__all__'

class PubGriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = PubGrief
        fields = '__all__'

class PubLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PubLevel
        fields = '__all__'