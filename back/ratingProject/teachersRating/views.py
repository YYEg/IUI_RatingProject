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

class EmployeeApiView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class DepartmentApiView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

from django.db.models import Sum

class DepartmentRatingApiView(APIView):
    def get(self, request):
        # Получаем список кафедр с их общим рейтингом (сумма достижений всех сотрудников)
        departments = Department.objects.annotate(
            total_score=Sum('employee__employee_achievment__score')  # Сумма баллов всех достижений сотрудников кафедры
        ).values('id', 'name', 'total_score')

        # Заполняем данные для вывода
        department_data = [
            {
                'id': department['id'],
                'name': department['name'],
                'sum': department['total_score'] or 0,  # Если сумма None, подставляем 0
                'rating': 0  # Пока рейтинг статичен, выставляем 0
            }
            for department in departments
        ]

        return Response(department_data)


class DepartmentApiViewDetail(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'id'

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
            verif_doc=request.data['verif_doc']
        )
        
        return Response({'Новое достижение': model_to_dict(ach_new)})

    
    def delete(self, request, pk):
        # Находим объект по его id
        achievment = get_object_or_404(Employee_Achievment, pk=pk)
        # Удаляем найденный объект
        achievment.delete()
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
            'department': user.department_id_id,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'employee': user.employee_id
        }
        return Response(user_data)
