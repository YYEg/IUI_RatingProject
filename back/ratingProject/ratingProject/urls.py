from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from teachersRating.views import Logout, PubGriefApiView, PubLevelApiView, PubTypeApiView, UserProfileView, \
    EmployeeRankingView, DepartmentRankingView, DepartmentEmployeeRankingView, OneDepartmentView, EmployeeAchievementsView, \
        AddAchievementFileView, AchievementsListView, OneAchievmentApiView, EmployeeAchievementsByFlagView, OneEmployeeView, \
            AddAchievementPublicationView;


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/token', obtain_auth_token, name='token'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),

    path('api/v1/pub_types/', PubTypeApiView.as_view(), name='pub_types'),
    path('api/v1/pub_griefs/', PubGriefApiView.as_view(), name='pub_griefs'),
    path('api/v1/pub_levels/', PubLevelApiView.as_view(), name='pub_levels'),

    path('api/v1/departments/<int:id>/', OneDepartmentView.as_view(), name='one_department'),
    path('api/v1/employees/<int:id>/', OneEmployeeView.as_view(), name='one_employee'),
    path('api/v1/achievements/', AchievementsListView.as_view(), name='achievements'),
    path('api/v1/achievements/<int:id>/', OneAchievmentApiView.as_view(), name='one_achievment'),

    path('api/v1/employee_ranking/', EmployeeRankingView.as_view(), name='employee_ranking'),
    path('api/v1/department_ranking/', DepartmentRankingView.as_view(), name='department_ranking'),
    path('api/v1/department_employee_ranking/<int:department_id>/', DepartmentEmployeeRankingView.as_view(), name='department_employee_ranking'),
    path('api/v1/employee_achievements/<int:employee_id>/', EmployeeAchievementsView.as_view(), name='employee_achievements'),
    path('api/v1/employees/<int:employee_id>/achievements/<str:is_pub>/<int:achievement_id>/', EmployeeAchievementsByFlagView.as_view(), name='employee_achievements_by_flag'),
    
    path('api/v1/add_achievement_file/', AddAchievementFileView.as_view(), name='add_achievement_file'),
    path('api/v1/add_achievement_publication/', AddAchievementPublicationView.as_view(), name='add_achievement_publication'),
     
    #  path('employee_achievments/update/<int:id>/', EmployeeAchievementUpdateView.as_view(), name='employee_achievment-update'),
    #  path('api/v1/update_message/<int:achievement_id>/', UpdateMessage.as_view(), name='update_message_employee_achievement'),
    # path('api/v1/employees/', EmployeeApiView.as_view()),
    # path('api/v1/departments/', DepartmentApiView.as_view()),
    # path('api/v1/departments/<int:id>/', DepartmentApiViewDetail.as_view()),
    # path('api/v1/employees/<int:id>/', EmployeeApiViewDetail.as_view()),
    # path('api/v1/achievments/', AchievmentApiView.as_view()),
    # path('api/v1/employee_achievment/', Employee_AchievmentApiView.as_view()),
    # path('employee_achievments/<int:id>/', EmployeeAchievementDetailView.as_view(), name='employee-achievement-detail'),
    # path('api/v1/department_ratings/', DepartmentRatingApiView.as_view(), name='department_ratings'),
    # path('api/v1/departments/<int:department_id>/teachers/', DepartmentTeachersApiView.as_view(), name='department_teachers'),
    #  path('api/v1/employee_achievment/', Employee_AchievmentApiView.as_view(), name='employee-achievment-detail'),
    #  path('employee_achievments/<int:id>/', Employee_AchievmentApiView.as_view(), name='employee_achievment_detail'),
    #  path('api/v1/delete_employee_achievement/<int:achievement_id>/', DeleteEmployeeAchievementApiView.as_view(), name='delete_employee_achievement'),
    #  path('api/v1/employee_achievements/teachers/<int:employee_id>/', EmployeeAchievementsApiView.as_view(), name='achivments_of_employee'),
    #  path('api/v1/employee_achievements/teachers/<int:employee_id>/delete', EmployeeAchievementsApiView.as_view(), name='achivments_of_employee'),
    #  path('api/v1/generate_report/', generate_report, name='generate_report'),
    #  path('api/v1/employe_achievments/employee/<int:employee_id>', ProfileEmployeeAchievementsApiView.as_view(), name='profile_employee_achievments'), #+
    #  path('api/employee/<employee_id>/achievement/<achievment_id>/achievements/', EmployeeAchievementByAchievmentApiView.as_view(), name='employee_achievment_achievment'),
    #  path('download/<int:achievement_record_id>/', DownloadAchievementDocumentApiView.as_view(), name='download_achievement_document'),
    #  path('api/v1/achievments/<int:achievment_id>', OneAchievmentApiView.as_view(), name='one_achievment'),
    #  path('api/v1/generate_personal_report/', GenearatePersonalReportApiView.as_view(), name='generate_report'),
]
