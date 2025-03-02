from .generate_personal_report import generate_personal_report
from rest_framework import generics, parsers
from .models import Employee, Department, Employee_Achievment, Achievment
from .serializers import DepartmentSerializer, Employee_AchievmentSerializer, AchievmentSerializer
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
                'email': employee.email,
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
                'email': teacher.email,
                'total_score': teacher.total_score or 0  # Если сумма None, подставляем 0
            }
            for teacher in teachers
        ]

        return Response(teacher_data)

class EmployeeApiViewDetail(APIView):
    def get(self, request, id):
        # Получаем сотрудника или возвращаем 404
        employee = get_object_or_404(Employee, id=id)
        
        # Формируем ответ с данными о сотруднике и его кафедре
        data = {
            "id": employee.id,
            "name": employee.name,
            "surname": employee.surname,
            "parentName": employee.parentName,
            'email': employee.email,
            "department": {
                "id": employee.department.id,
                "name": employee.department.name
            }
        }
        
        return Response(data)

class OneAchievmentApiView(APIView):
    def get(self, request, achievment_id):
        # Получаем сотрудника или возвращаем 404
        achievment = get_object_or_404(Achievment, id=achievment_id)
        
        # Формируем ответ с данными о сотруднике и его кафедре
        data = {
            "id": achievment.id,
            "name": achievment.name,
            "meas_unit_score": achievment.meas_unit_score,
        }
        
        return Response(data)

class Employee_AchievmentApiView(generics.ListCreateAPIView):
    queryset = Employee_Achievment.objects.all()
    serializer_class = Employee_AchievmentSerializer
    parser_classes = [parsers.MultiPartParser]  # Указываем парсер для обработки загрузки файлов

    def post(self, request):
        # Получаем экземпляр Employee по ID
        employee = get_object_or_404(Employee, id=request.data['employee'])

        # Получаем экземпляр Achievment по ID
        achievment = get_object_or_404(Achievment, id=request.data['achievment'])

        # Если файл загружается, он будет доступен через request.FILES['verif_doc']
        verif_doc = request.FILES.get('verif_doc')

        # Создаем новый объект Employee_Achievment
        ach_new = Employee_Achievment.objects.create(
            employee=employee,
            achievment=achievment,
            meas_unit_val=request.data['meas_unit_val'],
            score=request.data['score'],
            verif_doc=verif_doc,  # Загрузка файла
            verif_link=request.data['verif_link'],
            full_achivment_name=request.data['full_achivment_name'],
            reciving_date=request.data['reciving_date']
        )

        return Response({'Новое достижение': Employee_AchievmentSerializer(ach_new).data})
    
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
        
        # Получаем email из тела запроса
        email = request.data.get('email')
        
        if email:
            # Отправка сообщения об удалении
            yag = yagmail.SMTP('rezervdesu15@gmail.com', 'ddvd jduu prdi ktih')  
            yag.send(
                email,  # Используем email из запроса
                f"Удаление достижения", 
                f"Достижение {achievement.full_achivment_name} было удалено ввиду его некорректности, исправьте ошибки и внесите корректное достижение"
            )
        
        achievement.delete()

        return Response({'message': 'Достижение удалено!'}, status=status.HTTP_204_NO_CONTENT)

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
            'employee': user.employee_id,
            'role': user.role
        }
        return Response(user_data)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Employee, Employee_Achievment, Achievment
from django.db.models import Sum

class ProfileEmployeeAchievementsApiView(APIView):
    def get(self, request, employee_id):
        """Возвращает список всех достижений сотрудника, суммируя баллы, если они есть у сотрудника."""
        employee = get_object_or_404(Employee, id=employee_id)
        all_achievements = Achievment.objects.all()

        # Получаем достижения сотрудника
        employee_achievements = Employee_Achievment.objects.filter(employee=employee)

        # Создаем словарь для суммирования баллов по каждому достижению
        achievements_score = {}

        # Суммируем баллы для каждого достижения
        for emp_ach in employee_achievements:
            if emp_ach.achievment.id not in achievements_score:
                achievements_score[emp_ach.achievment.id] = 0
            achievements_score[emp_ach.achievment.id] += emp_ach.score  # Суммируем баллы для достижения

        # Создаем словарь для хранения баллов родительских достижений
        parent_achievements_score = {}

        # Проходим по всем достижениям и суммируем баллы для родительских достижений
        for achievement in all_achievements:
            if achievement.parent_id:  # Если у достижения есть родитель
                if achievement.parent_id not in parent_achievements_score:
                    parent_achievements_score[achievement.parent_id] = 0
                # Добавляем баллы дочернего достижения к родительскому
                parent_achievements_score[achievement.parent_id] += achievements_score.get(achievement.id, 0)

        # Обновляем баллы для родительских достижений
        for parent_id, score in parent_achievements_score.items():
            if parent_id in achievements_score:
                achievements_score[parent_id] += score
            else:
                achievements_score[parent_id] = score

        achievements_data = []

        for achievement in all_achievements:
            # Получаем суммарные баллы для текущего достижения
            total_score = achievements_score.get(achievement.id, 0)  # Если достижения нет у сотрудника, ставим 0

            # Добавляем достижение с нужными данными
            achievements_data.append({
                'id': achievement.id,
                'number': achievement.number,
                'achievment_name': achievement.name,
                'score': total_score,  # Сумма баллов для достижения
                'meas_unit_val': None,  # Пример, если вам нужно оставить данные
                'verif_doc': None,  # Пример
                'meas_unit_score': achievement.meas_unit_score
            })

        return Response({'employee': employee.surname, 'achievements': achievements_data})
    
class EmployeeAchievementByAchievmentApiView(APIView):
    def get(self, request, employee_id, achievment_id):
        # Получаем сотрудника и достижение по ID
        employee = get_object_or_404(Employee, id=employee_id)
        achievment = get_object_or_404(Achievment, id=achievment_id)

        # Фильтруем достижения сотрудника, соответствующие данному достижению
        achievements = Employee_Achievment.objects.filter(employee=employee, achievment=achievment)

        # Если достижения не найдены
        if not achievements.exists():
            return Response({'error': 'Достижения не найдены для данного сотрудника и достижения'}, status=404)

        # Сериализуем данные
        achievements_data = [
            {
                'id': ach.id,
                'employee_id': ach.employee.id,
                'achievment_name': ach.achievment.name,
                'full_name': ach.full_achivment_name,
                'score': ach.score,
                'meas_unit_val': ach.meas_unit_val,
                'verif_doc': ach.verif_doc.url if ach.verif_doc else None,  # Передаем URL файла или None
                'verif_link': ach.verif_link
                # Добавьте остальные поля по необходимости
            }
            for ach in achievements
        ]

        return Response({'employee': employee.surname, 'achievment': achievment.name, 'achievements': achievements_data})
   
class DownloadAchievementDocumentApiView(APIView):
    def get(self, request, achievement_record_id):
        # Получаем запись достижения по ID
        achievement_record = get_object_or_404(Employee_Achievment, id=achievement_record_id)

        # Проверяем, есть ли файл
        if not achievement_record.verif_doc:
            return Response({'error': 'Документ не найден'}, status=404)

        # Открываем файл и создаем ответ с файлом
        document_path = achievement_record.verif_doc.path  # Получаем путь к файлу
        document_name = achievement_record.verif_doc.name.split('/')[-1]  # Получаем имя файла

        # Отправляем файл пользователю
        return FileResponse(open(document_path, 'rb'), as_attachment=True, filename=document_name)

class GenearatePersonalReportApiView(APIView):
    def get(self, request, *args, **kwargs):
        response = generate_personal_report(request)
        return response