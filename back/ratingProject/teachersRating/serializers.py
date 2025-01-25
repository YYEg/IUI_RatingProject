from rest_framework import serializers
from .models import Teacher, Department, Teacher_Achivment, Achivment, Achivment_Category, Score_Value

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name', 'surname', 'parentName', 'department_id')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')

class Teacher_AchivmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher_Achivment
        fields = ('id', 'Achivment_id', 'teacher_id')

class AchivmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achivment
        fields = ('id', 'name', 'achivments_category_id')

class Achivment_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Achivment_Category
        fields = ('id', 'name')

class Score_ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score_Value
        fields = ('id', 'score', 'Achivment')