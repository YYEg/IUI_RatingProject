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
from rest_framework.views import APIView
from datetime import datetime

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
        period = request.query_params.get('period')
        if period:
            start_date, end_date = period.split('-')
            start_date = datetime.strptime(start_date, '%d.%m.%Y')
            end_date = datetime.strptime(end_date, '%d.%m.%Y')
            file_score_filter = Q(employee__employee_achievment_file__active=True, employee__employee_achievment_file__reciving_date__range=(start_date, end_date))
            pub_score_filter = Q(employee__employee_achievment_publication__active=True, employee__employee_achievment_publication__reciving_date__range=(start_date, end_date))
        else:
            file_score_filter = Q(employee__employee_achievment_file__active=True)
            pub_score_filter = Q(employee__employee_achievment_publication__active=True)
        department_scores = Department.objects.annotate(
            total_score=Sum('employee__employee_achievment_file__score', filter=file_score_filter, default=0) +
                        Sum('employee__employee_achievment_publication__score', filter=pub_score_filter, default=0),
        ).annotate(
            rank=Window(
                expression=Rank(),
                order_by=F('total_score').desc()
            )
        ).order_by('-total_score')

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
        period = request.query_params.get('period')
        start_date, end_date = period.split('-')
        start_date = datetime.strptime(start_date, '%d.%m.%Y')
        end_date = datetime.strptime(end_date, '%d.%m.%Y')

        employee_scores = Employee.objects.annotate(
            total_score=Sum('employee_achievment_file__score', filter=Q(employee_achievment_file__active=True, employee_achievment_file__reciving_date__range=(start_date, end_date)), default=0) +
                        Sum('employee_achievment_publication__score', filter=Q(employee_achievment_publication__active=True, employee_achievment_publication__reciving_date__range=(start_date, end_date)), default=0),
            total_unver_score=Sum('employee_achievment_file__score', default=0) + Sum('employee_achievment_publication__score', default=0),
        ).annotate(
            rank=Window(
                expression=Rank(),
                order_by=F('total_score').desc()
            )
        ).order_by('-total_score')

        result = [
            {
                'employee_id': employee.id,
                'surname': employee.surname,
                'name': employee.name,
                'total_score': employee.total_score if employee.total_score is not None else 0,
                'total_unver_score': employee.total_unver_score if employee.total_unver_score is not None else 0,
                'rank': employee.rank
            }
            for employee in employee_scores
        ]

        return Response(result)

#Рейтинг сотрудников внутри одного подразделения
class DepartmentEmployeeRankingView(APIView):
    def get(self, request, department_id):
        period = request.query_params.get('period')
        if period:
            start_date, end_date = period.split('-')
            start_date = datetime.strptime(start_date, '%d.%m.%Y')
            end_date = datetime.strptime(end_date, '%d.%m.%Y')
            file_score_filter = Q(employee_achievment_file__active=True, employee_achievment_file__reciving_date__range=(start_date, end_date))
            pub_score_filter = Q(employee_achievment_publication__active=True, employee_achievment_publication__reciving_date__range=(start_date, end_date))
        else:
            file_score_filter = Q(employee_achievment_file__active=True)
            pub_score_filter = Q(employee_achievment_publication__active=True)
        employees = Employee.objects.filter(department_id=department_id).annotate(
            total_score=Sum('employee_achievment_file__score', filter=file_score_filter, default=0) +
                        Sum('employee_achievment_publication__score', filter=pub_score_filter, default=0),
            total_unver_score=Sum('employee_achievment_file__score', default=0) + Sum('employee_achievment_publication__score', default=0),
            ranking=Window(
                expression=Rank(),
                order_by=F('total_score').desc()
            )
        ).order_by('-total_score')

        employee_data = [
            {
                'id': employee.id,
                'surname': employee.surname,
                'name': employee.name,
                'parentName': employee.parentName,
                'total_score': employee.total_score if employee.total_score is not None else 0,
                'total_unver_score': employee.total_unver_score if employee.total_unver_score is not None else 0,
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
        period = request.query_params.get('period')
        if period:
            start_date, end_date = period.split('-')
            start_date = datetime.strptime(start_date, '%d.%m.%Y')
            end_date = datetime.strptime(end_date, '%d.%m.%Y')
            file_score_filter = Q(employee_achievment_file__employee_id=employee_id, employee_achievment_file__active=True, employee_achievment_file__reciving_date__range=(start_date, end_date))
            pub_score_filter = Q(employee_achievment_publication__employee_id=employee_id, employee_achievment_publication__active=True, employee_achievment_publication__reciving_date__range=(start_date, end_date))
        else:
            file_score_filter = Q(employee_achievment_file__employee_id=employee_id, employee_achievment_file__active=True)
            pub_score_filter = Q(employee_achievment_publication__employee_id=employee_id, employee_achievment_publication__active=True)
        achievements = Achievment.objects.all()
        achievements_with_scores = achievements.annotate(
            total_score=Sum(
                'employee_achievment_file__score',
                filter=file_score_filter,
                default=0
            ) + Sum(
                'employee_achievment_publication__score',
                filter=pub_score_filter,
                default=0
            ),
            total_all_score=Sum(
                'employee_achievment_file__score',
                filter=Q(employee_achievment_file__employee_id=employee_id, employee_achievment_file__reciving_date__range=(start_date, end_date)),
                default=0
            ) + Sum(
                'employee_achievment_publication__score',
                filter=Q(employee_achievment_publication__employee_id=employee_id, employee_achievment_publication__reciving_date__range=(start_date, end_date)),
                default=0
            )
        )
        achievement_data = [
            {
                'id': achievement.id,
                'name': achievement.name,
                'total_score': achievement.total_score if achievement.total_score is not None else 0,
                'total_all_score': achievement.total_all_score if achievement.total_all_score is not None else 0,
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
        period = request.query_params.get('period')
        if is_pub:
            # Если флаг is_pub равен True, ищем в Employee_Achievment_Publication
            if period:
                start_date, end_date = period.split('-')
                start_date = datetime.strptime(start_date, '%d.%m.%Y')
                end_date = datetime.strptime(end_date, '%d.%m.%Y')
                achievements = Employee_Achievment_Publication.objects.filter(employee_id=employee_id, achievment_id=achievement_id, reciving_date__range=(start_date, end_date))
            else:
                achievements = Employee_Achievment_Publication.objects.filter(employee_id=employee_id, achievment_id=achievement_id)
        else:
            # Если флаг is_pub равен False, ищем в Employee_Achievment_File
            if period:
                start_date, end_date = period.split('-')
                start_date = datetime.strptime(start_date, '%d.%m.%Y')
                end_date = datetime.strptime(end_date, '%d.%m.%Y')
                achievements = Employee_Achievment_File.objects.filter(employee_id=employee_id, achievment_id=achievement_id, reciving_date__range=(start_date, end_date))
            else:
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

# Уведомление на почту сотруднику
class UpdateMessage(APIView):

    def get(self, request, achievement_id, is_pub):
        # Проверяем, находится ли достижение в нужной таблице
        if is_pub == 'true':
            achievement = Employee_Achievment_Publication.objects.filter(id=achievement_id).first()
        else:
            achievement = Employee_Achievment_File.objects.filter(id=achievement_id).first()
        
        if not achievement:
            return Response({'error': 'Достижение не найдено'}, status=status.HTTP_404_NOT_FOUND)

        # Получаем email и причину из query-параметров
        email = request.query_params.get('email')
        reason = request.query_params.get('reason')

        if email:
            yag = yagmail.SMTP('rezervdesu15@gmail.com', 'ddvd jduu prdi ktih')
            yag.send(
                email,
                f"Вам необходимо обновить достижения {achievement.full_achivment_name}", 
                f"Достижение {achievement.full_achivment_name} нуждается в редактировании\nЧто необходимо отредактировать: {reason}"
            )

        return Response({'message': 'Уведомление отправлено!'}, status=status.HTTP_200_OK)

# Удаление достижения сотрудника    
class DeleteAchievementView(APIView):
    def delete(self, request, achievement_id, is_pub):
        # Проверяем, находится ли достижение в нужной таблице
        if is_pub == 'true':
            achievement = Employee_Achievment_Publication.objects.filter(id=achievement_id).first()
        else:
            achievement = Employee_Achievment_File.objects.filter(id=achievement_id).first()
        
        if not achievement:
            return Response({'error': 'Достижение не найдено'}, status=status.HTTP_404_NOT_FOUND)

        # Получаем email из тела запроса
        email = request.data.get('email')
        reason = request.data.get('reason')

        if email:
            # Отправка сообщения об удалении
            yag = yagmail.SMTP('rezervdesu15@gmail.com', 'ddvd jduu prdi ktih')
            yag.send(
                email,
                f"Удаление достижения {achievement.full_achivment_name}", 
                f"Достижение {achievement.full_achivment_name} было удалено ввиду его некорректности, исправьте ошибки и внесите корректное достижение\nПричина удаления: {reason}"
            )

        # Удаляем достижение
        achievement.delete()

        return Response({'message': 'Достижение удалено!'}, status=status.HTTP_204_NO_CONTENT)

# Редактирование достижений
class EditAchievementView(APIView):
    def put(self, request, achievement_id, is_pub):
        # Проверяем, находится ли достижение в нужной таблице
        if is_pub == 'true':
            achievement = Employee_Achievment_Publication.objects.filter(id=achievement_id).first()
        else:
            achievement = Employee_Achievment_File.objects.filter(id=achievement_id).first()
        
        if not achievement:
            return Response({'error': 'Достижение не найдено'}, status=status.HTTP_404_NOT_FOUND)

        # Используем текущее значение employee из объекта achievement
        employee = achievement.employee

        # Проверка формата даты
        conference_date = request.data.get('conference_date')
        publication_data = request.data.get('publication_data')
        try:
            if conference_date:
                datetime.strptime(conference_date, '%Y-%m-%d')
            if publication_data:
                datetime.strptime(publication_data, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Неправильный формат date. Используйте один из этих форматов: YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        # Обновляем данные достижения
        serializer = Employee_Achievment_FileSerializer(achievement, data=request.data) if isinstance(achievement, Employee_Achievment_File) else Employee_Achievment_PublicationSerializer(achievement, data=request.data)
        
        if serializer.is_valid():
            serializer.save(employee=employee)  # Передаем employee в save
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Получение информации о достижении
class AchievementDetailView(APIView):
    def get(self, request, achievement_id, is_pub):
        # Проверяем, находится ли достижение в нужной таблице
        if is_pub == 'true':
            achievement = Employee_Achievment_Publication.objects.filter(id=achievement_id).first()
        else:
            achievement = Employee_Achievment_File.objects.filter(id=achievement_id).first()
        
        if not achievement:
            return Response({'error': 'Достижение не найдено'}, status=status.HTTP_404_NOT_FOUND)

        # Выбираем соответствующий сериализатор
        serializer = Employee_Achievment_FileSerializer(achievement) if isinstance(achievement, Employee_Achievment_File) else Employee_Achievment_PublicationSerializer(achievement)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# Скачивание отчета по сотруднику
class GenearatePersonalReportApiView(APIView):
    def get(self, request, *args, **kwargs):
        response = generate_personal_report(request)
        return response

# Подтверждение достижения
class ConfirmAchievementView(APIView):
    def post(self, request, achievement_id, is_pub):
        # Проверяем, находится ли достижение в нужной таблице
        if is_pub == 'true':
            achievement = Employee_Achievment_Publication.objects.filter(id=achievement_id).first()
        else:
            achievement = Employee_Achievment_File.objects.filter(id=achievement_id).first()
        
        if not achievement:
            return Response({'error': 'Достижение не найдено'}, status=status.HTTP_404_NOT_FOUND)

        # Обновляем поле active на true
        achievement.active = True
        achievement.save()

        return Response({'message': 'Достижение подтверждено!'}, status=status.HTTP_200_OK)

# Снятие подтверждения достижения
class UnConfirmAchievementView(APIView):
    def post(self, request, achievement_id, is_pub):
        # Проверяем, находится ли достижение в нужной таблице
        if is_pub == 'true':
            achievement = Employee_Achievment_Publication.objects.filter(id=achievement_id).first()
        else:
            achievement = Employee_Achievment_File.objects.filter(id=achievement_id).first()
        
        if not achievement:
            return Response({'error': 'Достижение не найдено'}, status=status.HTTP_404_NOT_FOUND)

        # Обновляем поле active на true
        achievement.active = False
        achievement.save()

        return Response({'message': 'Достижение подтверждено!'}, status=status.HTTP_200_OK)
