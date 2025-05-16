
# class DownloadAchievementDocumentApiView(APIView):
#     def get(self, request, achievement_record_id):
#         # Получаем запись достижения по ID
#         achievement_record = get_object_or_404(Employee_Achievment, id=achievement_record_id)

#         # Проверяем, есть ли файл
#         if not achievement_record.verif_doc:
#             return Response({'error': 'Документ не найден'}, status=404)

#         # Открываем файл и создаем ответ с файлом
#         document_path = achievement_record.verif_doc.path  # Получаем путь к файлу
#         document_name = achievement_record.verif_doc.name.split('/')[-1]  # Получаем имя файла

#         # Отправляем файл пользователю
#         return FileResponse(open(document_path, 'rb'), as_attachment=True, filename=document_name)

# class GenearatePersonalReportApiView(APIView):
#     def get(self, request, *args, **kwargs):
#         response = generate_personal_report(request)
#         return response