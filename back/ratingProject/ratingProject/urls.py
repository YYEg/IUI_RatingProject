from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from teachersRating.views import Logout, PubGriefApiView, PubLevelApiView, PubTypeApiView, UserProfileView, \
    EmployeeRankingView, DepartmentRankingView, DepartmentEmployeeRankingView, OneDepartmentView, EmployeeAchievementsView, \
        AddAchievementFileView, AchievementsListView, OneAchievmentApiView, EmployeeAchievementsByFlagView, OneEmployeeView, \
            AddAchievementPublicationView, UpdateMessage, DeleteAchievementView, EditAchievementView, AchievementDetailView, GenearatePersonalReportApiView;




urlpatterns = [
    # Аутентификация и профиль
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/token', obtain_auth_token, name='token'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),

    #Доп инфа публикаций
    path('api/v1/pub_types/', PubTypeApiView.as_view(), name='pub_types'),
    path('api/v1/pub_griefs/', PubGriefApiView.as_view(), name='pub_griefs'),
    path('api/v1/pub_levels/', PubLevelApiView.as_view(), name='pub_levels'),

    #Простые апи
    path('api/v1/departments/<int:id>/', OneDepartmentView.as_view(), name='one_department'),
    path('api/v1/employees/<int:id>/', OneEmployeeView.as_view(), name='one_employee'),
    path('api/v1/achievements/', AchievementsListView.as_view(), name='achievements'),
    path('api/v1/achievements/<int:id>/', OneAchievmentApiView.as_view(), name='one_achievment'),

    # Сложные апи
    path('api/v1/employee_ranking/', EmployeeRankingView.as_view(), name='employee_ranking'),
    path('api/v1/department_ranking/', DepartmentRankingView.as_view(), name='department_ranking'),
    path('api/v1/department_employee_ranking/<int:department_id>/', DepartmentEmployeeRankingView.as_view(), name='department_employee_ranking'),
    path('api/v1/employee_achievements/<int:employee_id>/', EmployeeAchievementsView.as_view(), name='employee_achievements'),
    path('api/v1/employees/<int:employee_id>/achievements/<str:is_pub>/<int:achievement_id>/', EmployeeAchievementsByFlagView.as_view(), name='employee_achievements_by_flag'),
    path('api/v1/achievement/<int:achievement_id>/<str:is_pub>/', AchievementDetailView.as_view(), name='achievement_detail'),
    
    # Добавление, удаление, обновление
    path('api/v1/add_achievement_file/', AddAchievementFileView.as_view(), name='add_achievement_file'),
    path('api/v1/add_achievement_publication/', AddAchievementPublicationView.as_view(), name='add_achievement_publication'),
    path('api/v1/delete_achievement/<int:achievement_id>/<str:is_pub>/', DeleteAchievementView.as_view(), name='delete_achievement'),
    path('api/v1/edit_achievement/<int:achievement_id>/<str:is_pub>/', EditAchievementView.as_view(), name='edit_achievement'),

    # Уведомление
    path('api/v1/update_message/<int:achievement_id>/<str:is_pub>/', UpdateMessage.as_view(), name='update_message'),
    
    # Генерация отчетов 
    path('api/v1/generate_personal_report/', GenearatePersonalReportApiView.as_view(), name='generate_report'),
    #path('api/v1/generate_report/', generate_report, name='generate_report'),
    #  path('download/<int:achievement_record_id>/', DownloadAchievementDocumentApiView.as_view(), name='download_achievement_document'),
    
]
