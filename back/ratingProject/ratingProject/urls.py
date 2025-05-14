from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from teachersRating.views import Logout, EmployeeAchievementDetailView, UpdateMessage, EmployeeAchievementUpdateView, PubGriefApiView, PubLevelApiView, PubTypeApiView, DataciteDoiView, GenearatePersonalReportApiView, OneAchievmentApiView, ProfileEmployeeAchievementsApiView, DownloadAchievementDocumentApiView, EmployeeAchievementByAchievmentApiView, EmployeeAchievementsApiView, DeleteEmployeeAchievementApiView, DepartmentRatingApiView, DepartmentTeachersApiView, UserProfileView, AchievmentApiView, EmployeeAchievmentApiView, EmployeeApiViewDetail, DepartmentApiViewDetail, DepartmentApiView, EmployeeApiView
from teachersRating.generate_report import generate_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/employees/', EmployeeApiView.as_view()),
    path('api/v1/departments/', DepartmentApiView.as_view()),
    path('api/v1/departments/<int:id>/', DepartmentApiViewDetail.as_view()),
    path('api/v1/employees/<int:id>/', EmployeeApiViewDetail.as_view()),
    path('api/v1/achievments/', AchievmentApiView.as_view()),
    # Унифицированные маршруты для достижений сотрудников
    path('api/v1/employee-achievements/', EmployeeAchievmentApiView.as_view(), name='employee_achievements_list_create'),
    path('api/v1/employee-achievements/<int:id>/', EmployeeAchievementDetailView.as_view(), name='employee_achievement_detail'),
    path('api/v1/employee-achievements/<int:id>/update/', EmployeeAchievementUpdateView.as_view(), name='employee_achievement_update'),
    path('api/v1/employee-achievements/<int:id>/delete/', DeleteEmployeeAchievementApiView.as_view(), name='employee_achievement_delete'),
    path('api/v1/employee-achievements/teachers/<int:employee_id>/', EmployeeAchievementsApiView.as_view(), name='employee_achievements_of_employee'),
    path('api/v1/employee-achievements/teachers/<int:employee_id>/delete/', EmployeeAchievementsApiView.as_view(), name='employee_achievements_of_employee_delete'),
    path('api/v1/employee-achievements/by-achievement/<int:employee_id>/<int:achievment_id>/', EmployeeAchievementByAchievmentApiView.as_view(), name='employee_achievement_by_achievment'),
    path('api/v1/employee-achievements/profile/<int:employee_id>/', ProfileEmployeeAchievementsApiView.as_view(), name='profile_employee_achievements'),
    path('api/v1/employee-achievements/<int:achievement_record_id>/download/', DownloadAchievementDocumentApiView.as_view(), name='download_achievement_document'),
    path('api/v1/achievments/<int:achievment_id>/', OneAchievmentApiView.as_view(), name='one_achievment'),
    path('api/v1/department-ratings/', DepartmentRatingApiView.as_view(), name='department_ratings'),
    path('api/v1/departments/<int:department_id>/teachers/', DepartmentTeachersApiView.as_view(), name='department_teachers'),
    path('auth/', include('djoser.urls')),
    path('auth/token', obtain_auth_token, name='token'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('api/v1/generate-report/', GenearatePersonalReportApiView.as_view(), name='generate_report'),
    path('api/v1/update-message/<int:achievement_id>/', UpdateMessage.as_view(), name='update_message_employee_achievement'),
    path('datacite-doi/<str:doi_first>/<str:doi_second>/', DataciteDoiView.as_view(), name='datacite-doi'),
    path('api/v1/pub-types/', PubTypeApiView.as_view(), name='pub_types'),
    path('api/v1/pub-griefs/', PubGriefApiView.as_view(), name='pub_griefs'),
    path('api/v1/pub-levels/', PubLevelApiView.as_view(), name='pub_levels'),
]
