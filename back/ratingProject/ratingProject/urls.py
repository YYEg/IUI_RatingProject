from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from teachersRating.views import Logout, UserProfileView, AchivmentApiView, Teacher_AchivmentApiView, Achivment_Category, TeacherApiViewDetail, DepartmentApiViewDetail, DepartmentApiView, TeacherApiView, Score_Value
from teachersRating.generate_report import generate_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/teachers/', TeacherApiView.as_view()),
    path('api/v1/departments/', DepartmentApiView.as_view()),
    path('api/v1/departments/<int:id>/', DepartmentApiViewDetail.as_view()),
    path('api/v1/teachers/<int:id>/', TeacherApiViewDetail.as_view()),
    path('api/v1/achivments_category/', Achivment_Category.as_view()),
    path('api/v1/achivments/', AchivmentApiView.as_view()),
    path('api/v1/teacher_achivments/', Teacher_AchivmentApiView.as_view()),
    path('api/v1/score_values/', Score_Value.as_view()),

    path('auth/', include('djoser.urls')),
    path('auth/token', obtain_auth_token, name='token'),

    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),

     path('api/v1/teacher_achivments/<int:pk>/', Teacher_AchivmentApiView.as_view(), name='teacher-achivment-detail'),
     path('api/v1/generate_report/', generate_report, name='generate_report')
]
