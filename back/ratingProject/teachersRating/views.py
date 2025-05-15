from .generate_personal_report import generate_personal_report
from rest_framework import generics, parsers
from .models import Employee, Department, Employee_Achievment_File, Employee_Achievment_Publication, Achievment, Pub_Grief, Pub_Level, Pub_Type
from .serializers import DepartmentSerializer, Employee_Achievment_FileSerializer, Employee_Achievment_PublicationSerializer, AchievmentSerializer, EmployeeSerializer, PubLevelSerializer, PubGriefSerializer, PubTypeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models import F, Window
from django.db.models.functions import Rank
import yagmail
from django.http import FileResponse
import requests
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser

#Все достижения, кроме тех, где meas_unit_score равен 0
class AchievementsListView(generics.ListAPIView):
    serializer_class = AchievmentSerializer

    def get_queryset(self):
        # Возвращаем все достижения, кроме тех, где meas_unit_score равен 0
        return Achievment.objects.exclude(meas_unit_score=0)

# Одно подразделение
class OneDepartmentView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'id'

# Один сотрудник
class OneEmployeeView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'id'

# Рейтинг подразделений
class DepartmentRankingView(APIView):
    def get(self, request):
        # Подсчет суммы баллов для каждого подразделения из двух таблиц достижений
        department_scores = Department.objects.annotate(
            total_score=Sum('employee__employee_achievment_file__score', default=0) + Sum('employee__employee_achievment_publication__score', default=0)
        ).annotate(
            rank=Window(
                expression=Rank(),
                order_by=F('total_score').desc()
            )
        ).order_by('-total_score')

        # Формирование выходного JSON
        result = [
            {
                'department_id': department.id,
                'name': department.name,
                'total_score': department.total_score if department.total_score is not None else 0,
                'rank': department.rank
            }
            for department in department_scores
        ]

        return Response(result)

# Рейтинга сотурдников
class EmployeeRankingView(APIView):
    def get(self, request):
        # Подсчет суммы баллов для каждого сотрудника из двух таблиц достижений
        employee_scores = Employee.objects.annotate(
            total_score=Sum('employee_achievment_file__score', default=0) + Sum('employee_achievment_publication__score', default=0)
        ).annotate(
            rank=Window(
                expression=Rank(),
                order_by=F('total_score').desc()
            )
        ).order_by('-total_score')

        # Формирование выходного JSON
        result = [
            {
                'employee_id': employee.id,
                'surname': employee.surname,
                'name': employee.name,
                'total_score': employee.total_score if employee.total_score is not None else 0,
                'rank': employee.rank
            }
            for employee in employee_scores
        ]

        return Response(result)

#Рейтинг сотрудников внутри одного подразделения
class DepartmentEmployeeRankingView(APIView):
    def get(self, request, department_id):
        # Извлекаем сотрудников конкретного подразделения
        employees = Employee.objects.filter(department_id=department_id).annotate(
            total_score=Sum('employee_achievment_file__score', default=0) + Sum('employee_achievment_publication__score', default=0),
            ranking=Window(
                expression=Rank(),
                order_by=F('total_score').desc()
            )
        ).order_by('-total_score')

        # Формируем данные для ответа
        employee_data = [
            {
                'id': employee.id,
                'surname': employee.surname,
                'name': employee.name,
                'parentName': employee.parentName,
                'total_score': employee.total_score if employee.total_score is not None else 0,
                'ranking': employee.ranking
            }
            for employee in employees
        ]

        return JsonResponse(employee_data, safe=False)

class PubTypeApiView(generics.ListAPIView):
    queryset = Pub_Type.objects.all()
    serializer_class = PubTypeSerializer

class PubGriefApiView(generics.ListAPIView):
    queryset = Pub_Grief.objects.all()
    serializer_class = PubGriefSerializer

class PubLevelApiView(generics.ListAPIView):
    serializer_class = PubLevelSerializer

    def get_queryset(self):
        grief_id = self.request.query_params.get('grief_id')
        return Pub_Level.objects.filter(pub_grief_id=grief_id)

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
            'employee': user.employee_id,
            'role': user.role
        }
        return Response(user_data)

# Достижения сотрудника
class EmployeeAchievementsView(APIView):
    def get(self, request, employee_id):
        # Получаем все показатели
        achievements = Achievment.objects.all()

        # Аннотируем каждое достижение суммой баллов из двух таблиц
        achievements_with_scores = achievements.annotate(
            total_score=Sum(
                'employee_achievment_file__score',
                filter=Q(employee_achievment_file__employee_id=employee_id),
                default=0
            ) + Sum(
                'employee_achievment_publication__score',
                filter=Q(employee_achievment_publication__employee_id=employee_id),
                default=0
            )
        )

        # Формируем данные для ответа
        achievement_data = [
            {
                'id': achievement.id,
                'name': achievement.name,
                'total_score': achievement.total_score if achievement.total_score is not None else 0,
                'number': achievement.number,
            }
            for achievement in achievements_with_scores
        ]

        return Response(achievement_data)

# Одно достижение
class OneAchievmentApiView(generics.RetrieveAPIView):
    queryset = Achievment.objects.all()
    serializer_class = AchievmentSerializer
    lookup_field = 'id'

# Достижения по показателю для сотрудника
class EmployeeAchievementsByFlagView(APIView):
    def get(self, request, employee_id, achievement_id, is_pub):
        # Преобразуем строковое значение в логическое
        is_pub = is_pub.lower() == 'true'
        
        if is_pub:
            # Если флаг is_pub равен True, ищем в Employee_Achievment_Publication
            achievements = Employee_Achievment_Publication.objects.filter(employee_id=employee_id, achievment_id=achievement_id)
        else:
            # Если флаг is_pub равен False, ищем в Employee_Achievment_File
            achievements = Employee_Achievment_File.objects.filter(employee_id=employee_id, achievment_id=achievement_id)

        # Формируем данные для ответа
        achievement_data = [
            {
                'id': achievement.id,
                'full_achivment_name': achievement.full_achivment_name,
                'score': achievement.score,
                'reciving_date': achievement.reciving_date,
                'active': achievement.active
            }
            for achievement in achievements
        ]

        return Response(achievement_data)

# Добавление достижения с файлом сотруднику
class AddAchievementFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        employee_id = request.data.get('employee')
        achievment_id = request.data.get('achievment')

        # Получаем объекты Employee и Achievment или возвращаем 404
        employee = get_object_or_404(Employee, id=employee_id)
        achievment = get_object_or_404(Achievment, id=achievment_id)

        # Создаем новый объект Employee_Achievment_File
        serializer = Employee_Achievment_FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=employee, achievment=achievment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Добавление публикации сотруднику
class AddAchievementPublicationView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        employee_id = request.data.get('employee')
        achievment_id = request.data.get('achievment')

        # Получаем объекты Employee и Achievment или возвращаем 404
        employee = get_object_or_404(Employee, id=employee_id)
        achievment = get_object_or_404(Achievment, id=achievment_id)

        # Создаем новый объект Employee_Achievment_Publication
        serializer = Employee_Achievment_PublicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=employee, achievment=achievment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)