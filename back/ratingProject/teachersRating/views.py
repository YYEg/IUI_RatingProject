from django.forms import model_to_dict
from rest_framework import generics
from .models import Employee, Department, Employee_Achievment, Achievment
from .serializers import EmployeeSerializer, DepartmentSerializer, Employee_AchievmentSerializer, AchievmentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models import F, Window
from django.db.models.functions import Rank

# class EmployeeApiView(generics.ListAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer

class EmployeeApiView(APIView):
    def get(self, request):
        employees = Employee.objects.annotate(
            total_score=Sum('employee_achievment__score'),
            rating=Window(
                expression=Rank(),
                order_by=F('total_score').desc()
            )
        )

        employee_data = [
            {
                'id': employee.id,
                'surname': employee.surname,
                'name': employee.name,
                'parentName': employee.parentName,
                'total_score': employee.total_score or 0,
                'rating': employee.rating
            }
            for employee in employees
        ]

        return Response(employee_data)
    
class DepartmentApiView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentRatingApiView(APIView):
    def get(self, request):
        departments = Department.objects.annotate(
            total_score=Sum('employee__employee_achievment__score'),
            rating=Window(
                expression=Rank(),
                order_by=F('total_score').desc()
            )
        ).values('id', 'name', 'total_score', 'rating')

        department_data = [
            {
                'id': department['id'],
                'name': department['name'],
                'sum': department['total_score'] or 0,
                'rating': department['rating']
            }
            for department in departments
        ]

        return Response(department_data)


class DepartmentApiViewDetail(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'id'

class DepartmentTeachersApiView(APIView):
    def get(self, request, department_id):
        # Получаем кафедру или возвращаем 404
        department = get_object_or_404(Department, id=department_id)

        # Получаем преподавателей только этой кафедры с суммой их достижений
        teachers = Employee.objects.filter(department=department).annotate(
            total_score=Sum('employee_achievment__score')  # Суммируем баллы достижений
        )

        # Сериализуем данные
        teacher_data = [
            {
                'id': teacher.id,
                'surname': teacher.surname,
                'name': teacher.name,
                'parentName': teacher.parentName,
                'total_score': teacher.total_score or 0  # Если сумма None, подставляем 0
            }
            for teacher in teachers
        ]

        return Response(teacher_data)

class EmployeeApiViewDetail(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'id'

class Employee_AchievmentApiView(generics.ListCreateAPIView):
    queryset = Employee_Achievment.objects.all()
    serializer_class = Employee_AchievmentSerializer
    
    def post(self, request):
        # Получаем экземпляр Employee по ID
        employee = get_object_or_404(Employee, id=request.data['employee'])
        
        # Получаем экземпляр Achievment по ID
        achievment = get_object_or_404(Achievment, id=request.data['achievment'])

        # Создаем новый объект Employee_Achievment
        ach_new = Employee_Achievment.objects.create(
            employee=employee,
            achievment=achievment,
            meas_unit_val=request.data['meas_unit_val'],
            score=request.data['score'],
            verif_doc=request.data['verif_doc'],
            #number=request.data['number']
        )
        
        return Response({'Новое достижение': model_to_dict(ach_new)})
    
class EmployeeAchievementsApiView(APIView):
    def get(self, request, employee_id):
        """Возвращает список достижений конкретного сотрудника с их баллами."""
        employee = get_object_or_404(Employee, id=employee_id)
        achievements = Employee_Achievment.objects.filter(employee=employee)

        achievements_data = [
            {
                'id': ach.id,
                'achievment_name': ach.achievment.name,
                'score': ach.score,
                'meas_unit_val': ach.meas_unit_val,
                'verif_doc': ach.verif_doc,
                #'number': ach.number
            }
            for ach in achievements
        ]

        return Response({'employee': employee.surname, 'achievements': achievements_data})

    
    def delete(self, request, employee_id):
        achievments = Employee_Achievment.objects.filter(employee_id=employee_id)
        if not achievments.exists():
            return Response({'error': 'Достижения не найдены'}, status=404)

        achievments.delete()
        return Response({'message': 'Все достижения сотрудника удалены!'}, status=204)
    
class EmployeeAchievementsDeleteApiView(APIView):
    def get(self, request, employee_id):
        """Возвращает список достижений конкретного сотрудника с их баллами."""
        employee = get_object_or_404(Employee, id=employee_id)
        achievements = Employee_Achievment.objects.filter(employee=employee)

        achievements_data = [
            {
                'id': ach.id,
                'achievment_name': ach.achievment.name,
                'score': ach.score,
                'meas_unit_val': ach.meas_unit_val,
                'verif_doc': ach.verif_doc,
                #'number': ach.number
            }
            for ach in achievements
        ]

        return Response({'employee': employee.surname, 'achievements': achievements_data})

    def delete(self, request, achievement_id):
        """Удаляет конкретное достижение по его ID"""
        achievement = get_object_or_404(Employee_Achievment, id=achievement_id)
        achievement.delete()
        return Response({'message': 'Достижение удалено!'}, status=204)
    
class DeleteEmployeeAchievementApiView(APIView):
    """Удаляет конкретное достижение сотрудника по его ID"""

    def delete(self, request, achievement_id):
        achievement = get_object_or_404(Employee_Achievment, id=achievement_id)
        achievement.delete()
        return Response({'message': 'Достижение удалено!'}, status=204)

class AchievmentApiView(generics.ListAPIView):
    queryset = Achievment.objects.all()
    serializer_class = AchievmentSerializer

class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        user_data = {
            'username': user.username,
            'email': user.email,
            'department': user.department_id,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'employee': user.employee_id
        }
        return Response(user_data)
