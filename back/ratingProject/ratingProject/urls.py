from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from teachersRating.views import Logout, ProfileEmployeeAchievementsApiView, DownloadAchievementDocumentApiView, EmployeeAchievementByAchievmentApiView, EmployeeAchievementsApiView, EmployeeAchievementsDeleteApiView, DeleteEmployeeAchievementApiView, DepartmentRatingApiView, DepartmentTeachersApiView, UserProfileView, AchievmentApiView, Employee_AchievmentApiView, EmployeeApiViewDetail, DepartmentApiViewDetail, DepartmentApiView, EmployeeApiView
from teachersRating.generate_report import generate_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/employees/', EmployeeApiView.as_view()),
    path('api/v1/departments/', DepartmentApiView.as_view()),
    path('api/v1/departments/<int:id>/', DepartmentApiViewDetail.as_view()),
    path('api/v1/employees/<int:id>/', EmployeeApiViewDetail.as_view()),
    path('api/v1/achievments/', AchievmentApiView.as_view()),
    path('api/v1/employee_achievment/', Employee_AchievmentApiView.as_view()),
    path('api/v1/department_ratings/', DepartmentRatingApiView.as_view(), name='department_ratings'),
    path('api/v1/departments/<int:department_id>/teachers/', DepartmentTeachersApiView.as_view(), name='department_teachers'),

    path('auth/', include('djoser.urls')),
    path('auth/token', obtain_auth_token, name='token'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),

     path('api/v1/employee_achievment/', Employee_AchievmentApiView.as_view(), name='employee-achievment-detail'),
     path('api/v1/delete_employee_achievement/<int:achievement_id>/', DeleteEmployeeAchievementApiView.as_view(), name='delete_employee_achievement'),
     path('api/v1/employee_achievements/teachers/<int:employee_id>/', EmployeeAchievementsApiView.as_view(), name='achivments_of_employee'),
     path('api/v1/employee_achievements/teachers/<int:employee_id>/delete', EmployeeAchievementsApiView.as_view(), name='achivments_of_employee'),
     path('api/v1/generate_report/', generate_report, name='generate_report'),
     path('api/v1/employe_achievments/employee/<int:employee_id>', ProfileEmployeeAchievementsApiView.as_view(), name='profile_employee_achievments'),
     path('api/employee/<employee_id>/achievement/<achievment_id>/achievements/', EmployeeAchievementByAchievmentApiView.as_view(), name='employee_achievment_achievment'),
      path('download/<int:achievement_record_id>/', DownloadAchievementDocumentApiView.as_view(), name='download_achievement_document'),
]
