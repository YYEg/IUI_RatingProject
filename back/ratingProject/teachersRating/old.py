
# class EmployeeApiView(APIView):
#     def get(self, request):
#         employees = Employee.objects.annotate(
#             total_score=Sum('employee_achievment__score'),
#             rating=Window(
#                 expression=Rank(),
#                 order_by=F('total_score').desc()
#             )
#         )

#         employee_data = [
#             {
#                 'id': employee.id,
#                 'surname': employee.surname,
#                 'name': employee.name,
#                 'parentName': employee.parentName,
#                 'email': employee.email,
#                 'total_score': employee.total_score or 0,
#                 'rating': employee.rating
#             }
#             for employee in employees
#         ]

#         return Response(employee_data)
    
# class DepartmentApiView(generics.ListAPIView):
#     queryset = Department.objects.all()
#     serializer_class = DepartmentSerializer

# class DepartmentRatingApiView(APIView):
#     def get(self, request):
#         departments = Department.objects.annotate(
#             total_score=Sum('employee__employee_achievment__score'),
#             rating=Window(
#                 expression=Rank(),
#                 order_by=F('total_score').desc()
#             )
#         ).values('id', 'name', 'total_score', 'rating')

#         department_data = [
#             {
#                 'id': department['id'],
#                 'name': department['name'],
#                 'sum': department['total_score'] or 0,
#                 'rating': department['rating']
#             }
#             for department in departments
#         ]

#         return Response(department_data)

# class DepartmentApiViewDetail(generics.RetrieveAPIView):
#     queryset = Department.objects.all()
#     serializer_class = DepartmentSerializer
#     lookup_field = 'id'

# class DepartmentTeachersApiView(APIView):
#     def get(self, request, department_id):
#         # Получаем кафедру или возвращаем 404
#         department = get_object_or_404(Department, id=department_id)

#         # Получаем преподавателей только этой кафедры с суммой их достижений
#         teachers = Employee.objects.filter(department=department).annotate(
#             total_score=Sum('employee_achievment__score')  # Суммируем баллы достижений
#         )

#         # Сериализуем данные
#         teacher_data = [
#             {
#                 'id': teacher.id,
#                 'surname': teacher.surname,
#                 'name': teacher.name,
#                 'parentName': teacher.parentName,
#                 'email': teacher.email,
#                 'total_score': teacher.total_score or 0  # Если сумма None, подставляем 0
#             }
#             for teacher in teachers
#         ]

#         return Response(teacher_data)

# # class EmployeeApiViewDetail(APIView):
# #     def get(self, request, id):
# #         # Получаем сотрудника или возвращаем 404
# #         employee = get_object_or_404(Employee, id=id)
        
# #         # Формируем ответ с данными о сотруднике и его кафедре
# #         data = {
# #             "id": employee.id,
# #             "name": employee.name,
# #             "surname": employee.surname,
# #             "parentName": employee.parentName,
# #             'email': employee.email,
# #             "department": {
# #                 "id": employee.department.id,
# #                 "name": employee.department.name
# #             }
# #         }
        
# #         return Response(data)

# class OneAchievmentApiView(APIView):
#     def get(self, request, achievment_id):
#         # Получаем сотрудника или возвращаем 404
#         achievment = get_object_or_404(Achievment, id=achievment_id)
        
#         # Формируем ответ с данными о сотруднике и его кафедре
#         data = {
#             "id": achievment.id,
#             "name": achievment.name,
#             "meas_unit_score": achievment.meas_unit_score,
#             "is_pub": achievment.is_pub,
#             "has_publication": achievment.has_publication,
#             "has_conference": achievment.has_conference,
#             "meas_unit": achievment.meas_unit,
#             "verif_doc_info": achievment.verif_doc_info
#         }
        
#         return Response(data)

# # class EmployeeAchievementDetailView(generics.RetrieveAPIView):
# #     serializer_class = Employee_AchievmentSerializer
# #     lookup_field = 'id'

# #     def get_queryset(self):
# #         return Employee_Achievment.objects.filter(id=self.kwargs.get(self.lookup_field))


# # class Employee_AchievmentApiView(generics.ListCreateAPIView):
# #     queryset = Employee_Achievment.objects.all()
# #     serializer_class = Employee_AchievmentSerializer
# #     parser_classes = [parsers.MultiPartParser]  # Указываем парсер для обработки загрузки файлов

# #     def post(self, request):
# #         employee = get_object_or_404(Employee, id=request.data['employee'])
# #         achievment = get_object_or_404(Achievment, id=request.data['achievment'])
# #         # Если файл загружается, он будет доступен через request.FILES['verif_doc']
# #         verif_doc = request.FILES.get('verif_doc')
# #         # Получаем объекты Pub_Type, Pub_Grief и Pub_Level по их ID
# #         pub_type = get_object_or_404(Pub_Type, id=request.data.get('pub_type')) if request.data.get('pub_type') else None
# #         pub_grief = get_object_or_404(Pub_Grief, id=request.data.get('pub_grief')) if request.data.get('pub_grief') else None
# #         pub_level = get_object_or_404(Pub_Level, id=request.data.get('pub_level')) if request.data.get('pub_level') else None
# #         # Создаем новый объект Employee_Achievment с новыми полями
# #         ach_new = Employee_Achievment.objects.create(
# #             employee=employee,
# #             achievment=achievment,
# #             meas_unit_val=request.data['meas_unit_val'],
# #             score=request.data['score'],
# #             verif_doc=verif_doc,  # Загрузка файла
# #             verif_link=request.data['verif_link'],
# #             full_achivment_name=request.data['full_achivment_name'],
# #             reciving_date=request.data['reciving_date'],
# #             pub_type=pub_type,  # Передаем объект Pub_Type
# #             pub_grief=pub_grief,  # Передаем объект Pub_Grief
# #             pub_level=pub_level,  # Передаем объект Pub_Level
# #             pub_language=request.data.get('language_pub', ''),
# #             pub_doi=request.data.get('doi', ''),
# #             pub_authors_employees=request.data.get('empl_authors', ''),
# #             pub_authors_students=request.data.get('stud_authors', ''),
# #             pub_out_authors=request.data.get('out_authors', ''),
# #             bibliographic_desc=request.data.get('bibliographic', ''),
# #             publication_name=request.data.get('publication_name', ''),
# #             publicator=request.data.get('publicator', ''),
# #             publication_data=request.data.get('publication_date', None),
# #             publication_year_vol_num=request.data.get('yearVolNum', ''),
# #             conference_status=request.data.get('conference_status', ''),
# #             conference_date=request.data.get('conference_date', None),
# #             conference_name=request.data.get('conference_name', '')
# #         )

# #         return Response({'Новое достижение': Employee_AchievmentSerializer(ach_new).data})
    
# #     def put(self, request, id):
# #         try:
# #             # Получаем запись по ID
# #             achievement = get_object_or_404(Employee_Achievment, id=id)

# #             # Обновляем поля
# #             achievement.meas_unit_val = request.data.get('meas_unit_val', achievement.meas_unit_val)
# #             achievement.score = request.data.get('score', achievement.score)
# #             achievement.verif_link = request.data.get('verif_link', achievement.verif_link)
# #             achievement.full_achivment_name = request.data.get('full_achivment_name', achievement.full_achivment_name)
# #             achievement.reciving_date = request.data.get('reciving_date', achievement.reciving_date)

# #             # Обновляем связанные объекты
# #             if request.data.get('pub_type'):
# #                 achievement.pub_type = get_object_or_404(Pub_Type, id=request.data.get('pub_type'))
# #             if request.data.get('pub_grief'):
# #                 achievement.pub_grief = get_object_or_404(Pub_Grief, id=request.data.get('pub_grief'))
# #             if request.data.get('pub_level'):
# #                 achievement.pub_level = get_object_or_404(Pub_Level, id=request.data.get('pub_level'))

# #             # Обновляем остальные поля
# #             achievement.pub_language = request.data.get('language_pub', achievement.pub_language)
# #             achievement.pub_doi = request.data.get('doi', achievement.pub_doi)
# #             achievement.pub_authors_employees = request.data.get('empl_authors', achievement.pub_authors_employees)
# #             achievement.pub_authors_students = request.data.get('stud_authors', achievement.pub_authors_students)
# #             achievement.pub_out_authors = request.data.get('out_authors', achievement.pub_out_authors)
# #             achievement.bibliographic_desc = request.data.get('bibliographic', achievement.bibliographic_desc)
# #             achievement.publication_name = request.data.get('publication_name', achievement.publication_name)
# #             achievement.publicator = request.data.get('publicator', achievement.publicator)
# #             achievement.publication_data = request.data.get('publication_date', achievement.publication_data)
# #             achievement.publication_year_vol_num = request.data.get('yearVolNum', achievement.publication_year_vol_num)
# #             achievement.conference_status = request.data.get('conference_status', achievement.conference_status)
# #             achievement.conference_date = request.data.get('conference_date', achievement.conference_date)
# #             achievement.conference_name = request.data.get('conference_name', achievement.conference_name)

# #             # Если файл загружается, обновляем его
# #             if 'verif_doc' in request.FILES:
# #                 achievement.verif_doc = request.FILES['verif_doc']

# #             # Сохраняем изменения
# #             achievement.save()

# #             return Response({'Обновленное достижение': Employee_AchievmentSerializer(achievement).data}, status=status.HTTP_200_OK)

# #         except Exception as e:
# #             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # class EmployeeAchievementUpdateView(generics.UpdateAPIView):
# #     queryset = Employee_Achievment.objects.all()
# #     serializer_class = Employee_AchievmentSerializer
# #     parser_classes = [parsers.MultiPartParser]  # Для обработки загрузки файлов

# #     def put(self, request, *args, **kwargs):
# #         try:
# #             # Получаем ID из URL
# #             id = kwargs.get('id')
# #             achievement = get_object_or_404(Employee_Achievment, id=id)

# #             # Обновляем поля
# #             achievement.meas_unit_val = request.data.get('meas_unit_val', achievement.meas_unit_val)
# #             achievement.score = request.data.get('score', achievement.score)
# #             achievement.verif_link = request.data.get('verif_link', achievement.verif_link)
# #             achievement.full_achivment_name = request.data.get('full_achivment_name', achievement.full_achivment_name)
# #             achievement.reciving_date = request.data.get('reciving_date', achievement.reciving_date)

# #             # Обновляем связанные объекты
# #             if request.data.get('pub_type'):
# #                 achievement.pub_type = get_object_or_404(Pub_Type, id=request.data.get('pub_type'))
# #             if request.data.get('pub_grief'):
# #                 achievement.pub_grief = get_object_or_404(Pub_Grief, id=request.data.get('pub_grief'))
# #             if request.data.get('pub_level'):
# #                 achievement.pub_level = get_object_or_404(Pub_Level, id=request.data.get('pub_level'))

# #             # Обновляем остальные поля
# #             achievement.pub_language = request.data.get('language_pub', achievement.pub_language)
# #             achievement.pub_doi = request.data.get('doi', achievement.pub_doi)
# #             achievement.pub_authors_employees = request.data.get('empl_authors', achievement.pub_authors_employees)
# #             achievement.pub_authors_students = request.data.get('stud_authors', achievement.pub_authors_students)
# #             achievement.pub_out_authors = request.data.get('out_authors', achievement.pub_out_authors)
# #             achievement.bibliographic_desc = request.data.get('bibliographic', achievement.bibliographic_desc)
# #             achievement.publication_name = request.data.get('publication_name', achievement.publication_name)
# #             achievement.publicator = request.data.get('publicator', achievement.publicator)
# #             achievement.publication_data = request.data.get('publication_date', achievement.publication_data)
# #             achievement.publication_year_vol_num = request.data.get('yearVolNum', achievement.publication_year_vol_num)
# #             achievement.conference_status = request.data.get('conference_status', achievement.conference_status)
# #             achievement.conference_date = request.data.get('conference_date', achievement.conference_date)
# #             achievement.conference_name = request.data.get('conference_name', achievement.conference_name)

# #             # Если файл загружается, обновляем его
# #             if 'verif_doc' in request.FILES:
# #                 achievement.verif_doc = request.FILES['verif_doc']

# #             # Сохраняем изменения
# #             achievement.save()

# #             return Response(
# #                 {'Обновленное достижение': Employee_AchievmentSerializer(achievement).data},
# #                 status=status.HTTP_200_OK
# #             )

# #         except Exception as e:
# #             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

# # class EmployeeAchievementsApiView(APIView):
# #     def get(self, request, employee_id):
# #         """Возвращает список достижений конкретного сотрудника с их баллами."""
# #         employee = get_object_or_404(Employee, id=employee_id)
# #         achievements = Employee_Achievment.objects.filter(employee=employee)

# #         achievements_data = [
# #             {
# #                 'id': ach.id,
# #                 'achievment_name': ach.achievment.name,
# #                 'score': ach.score,
# #                 'meas_unit_val': ach.meas_unit_val,
# #                 'verif_doc': ach.verif_doc,
# #                 #'number': ach.number
# #             }
# #             for ach in achievements
# #         ]

# #         return Response({'employee': employee.surname, 'achievements': achievements_data})

    
# #     def delete(self, request, employee_id):
# #         achievments = Employee_Achievment.objects.filter(employee_id=employee_id)
# #         if not achievments.exists():
# #             return Response({'error': 'Достижения не найдены'}, status=404)

# #         achievments.delete()
# #         return Response({'message': 'Все достижения сотрудника удалены!'}, status=204)
    
# # class DeleteEmployeeAchievementApiView(APIView):
# #     """Удаляет конкретное достижение сотрудника по его ID"""

# #     def delete(self, request, achievement_id):
# #         achievement = get_object_or_404(Employee_Achievment, id=achievement_id)
        
# #         # Получаем email из тела запроса
# #         email = request.data.get('email')
# #         reason = request.data.get('reason')
        
# #         if email:
# #             # Отправка сообщения об удалении
# #             yag = yagmail.SMTP('rezervdesu15@gmail.com', 'ddvd jduu prdi ktih')  
# #             yag.send(
# #                 email,  # Используем email из запроса
# #                 f"Удаление достижения {achievement.full_achivment_name}", 
# #                 f"Достижение {achievement.full_achivment_name} было удалено ввиду его некорректности, исправьте ошибки и внесите корректное достижение\nПричина удаления: {reason}"
# #             )
        
# #         achievement.delete()

# #         return Response({'message': 'Достижение удалено!'}, status=status.HTTP_204_NO_CONTENT)
    
# # class UpdateMessage(APIView):

# #     def get(self, request, achievement_id):
# #         achievement = get_object_or_404(Employee_Achievment, id=achievement_id)
        
# #         # Получаем email и причину из query-параметров
# #         email = request.query_params.get('email')
# #         reason = request.query_params.get('reason')

# #         print(email)  # Для отладки
        
# #         if email:
# #             print('есть мыло')
# #             yag = yagmail.SMTP('rezervdesu15@gmail.com', 'ddvd jduu prdi ktih')
# #             yag.send(
# #                 email,
# #                 f"Вам необходимо обновить достижения {achievement.full_achivment_name}", 
# #                 f"Достижение {achievement.full_achivment_name} нуждается в редактировании\nЧто необходимо отредактировать: {reason}"
# #             )

# #         return Response({'message': 'Достижение удалено!'}, status=status.HTTP_204_NO_CONTENT)


# class AchievmentApiView(generics.ListAPIView):
#     queryset = Achievment.objects.all()
#     serializer_class = AchievmentSerializer

# # class ProfileEmployeeAchievementsApiView(APIView):
# #     def get(self, request, employee_id):
# #         """Возвращает список всех достижений сотрудника, суммируя баллы, если они есть у сотрудника."""
# #         employee = get_object_or_404(Employee, id=employee_id)
# #         all_achievements = Achievment.objects.all()

# #         # Получаем достижения сотрудника
# #         employee_achievements = Employee_Achievment.objects.filter(employee=employee)

# #         # Создаем словарь для суммирования баллов по каждому достижению
# #         achievements_score = {}

# #         # Суммируем баллы для каждого достижения
# #         for emp_ach in employee_achievements:
# #             if emp_ach.achievment.id not in achievements_score:
# #                 achievements_score[emp_ach.achievment.id] = 0
# #             achievements_score[emp_ach.achievment.id] += emp_ach.score  # Суммируем баллы для достижения

# #         # Создаем словарь для хранения баллов родительских достижений
# #         parent_achievements_score = {}

# #         # Проходим по всем достижениям и суммируем баллы для родительских достижений
# #         for achievement in all_achievements:
# #             if achievement.parent_id:  # Если у достижения есть родитель
# #                 if achievement.parent_id not in parent_achievements_score:
# #                     parent_achievements_score[achievement.parent_id] = 0
# #                 # Добавляем баллы дочернего достижения к родительскому
# #                 parent_achievements_score[achievement.parent_id] += achievements_score.get(achievement.id, 0)

# #         # Обновляем баллы для родительских достижений
# #         for parent_id, score in parent_achievements_score.items():
# #             if parent_id in achievements_score:
# #                 achievements_score[parent_id] += score
# #             else:
# #                 achievements_score[parent_id] = score

# #         achievements_data = []

# #         for achievement in all_achievements:
# #             # Получаем суммарные баллы для текущего достижения
# #             total_score = achievements_score.get(achievement.id, 0)  # Если достижения нет у сотрудника, ставим 0

# #             # Добавляем достижение с нужными данными
# #             achievements_data.append({
# #                 'id': achievement.id,
# #                 'number': achievement.number,
# #                 'achievment_name': achievement.name,
# #                 'score': total_score,  # Сумма баллов для достижения
# #                 'meas_unit_val': None,  # Пример, если вам нужно оставить данные
# #                 'verif_doc': None,  # Пример
# #                 'meas_unit_score': achievement.meas_unit_score
# #             })

# #         return Response({'employee': employee.surname, 'achievements': achievements_data})
    
# # class EmployeeAchievementByAchievmentApiView(APIView):
# #     def get(self, request, employee_id, achievment_id):
# #         # Получаем сотрудника и достижение по ID
# #         employee = get_object_or_404(Employee, id=employee_id)
# #         achievment = get_object_or_404(Achievment, id=achievment_id)

# #         # Фильтруем достижения сотрудника, соответствующие данному достижению
# #         achievements = Employee_Achievment.objects.filter(employee=employee, achievment=achievment)

# #         # Если достижения не найдены
# #         if not achievements.exists():
# #             return Response({'error': 'Достижения не найдены для данного сотрудника и достижения'}, status=404)

# #         # Сериализуем данные
# #         achievements_data = [
# #             {
# #                 'id': ach.id,
# #                 'employee_id': ach.employee.id,
# #                 'achievment_name': ach.achievment.name,
# #                 'full_name': ach.full_achivment_name,
# #                 'score': ach.score,
# #                 'meas_unit_val': ach.meas_unit_val,
# #                 'verif_doc': ach.verif_doc.url if ach.verif_doc else None,  # Передаем URL файла или None
# #                 'verif_link': ach.verif_link
# #                 # Добавьте остальные поля по необходимости
# #             }
# #             for ach in achievements
# #         ]

# #         return Response({'employee': employee.surname, 'achievment': achievment.name, 'achievements': achievements_data})
   
# # class DownloadAchievementDocumentApiView(APIView):
# #     def get(self, request, achievement_record_id):
# #         # Получаем запись достижения по ID
# #         achievement_record = get_object_or_404(Employee_Achievment, id=achievement_record_id)

# #         # Проверяем, есть ли файл
# #         if not achievement_record.verif_doc:
# #             return Response({'error': 'Документ не найден'}, status=404)

# #         # Открываем файл и создаем ответ с файлом
# #         document_path = achievement_record.verif_doc.path  # Получаем путь к файлу
# #         document_name = achievement_record.verif_doc.name.split('/')[-1]  # Получаем имя файла

# #         # Отправляем файл пользователю
# #         return FileResponse(open(document_path, 'rb'), as_attachment=True, filename=document_name)

# class GenearatePersonalReportApiView(APIView):
#     def get(self, request, *args, **kwargs):
#         response = generate_personal_report(request)
#         return response