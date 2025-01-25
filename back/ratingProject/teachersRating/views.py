from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics
from .models import Teacher, Department, Teacher_Achivment, Achivment, Achivment_Category, Score_Value
from .serializers import TeacherSerializer, DepartmentSerializer, Teacher_AchivmentSerializer, AchivmentSerializer, Achivment_CategorySerializer, Score_ValueSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class TeacherApiView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class DepartmentApiView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentApiViewDetail(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'id'  # Указываем поле, по которому будет происходить поиск

class TeacherApiViewDetail(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'id'  # Указываем поле, по которому будет происходить поиск

from django.shortcuts import get_object_or_404

class Teacher_AchivmentApiView(generics.ListCreateAPIView):
    queryset = Teacher_Achivment.objects.all()
    serializer_class = Teacher_AchivmentSerializer

    def post(self, request):
        # Получаем экземпляр учителя по teacher_id
        teacher = get_object_or_404(Teacher, id=request.data['teacher_id'])

        # Создаем новый объект Teacher_Achivment с полученными данными
        ach_new = Teacher_Achivment.objects.create(
            teacher_id=teacher,
            Achivment_id=request.data['Achivment'],
            score=request.data['score'],
        )
        
        return Response({'new_ach': model_to_dict(ach_new)})
    
    def delete(self, request, pk):
        # Находим объект Teacher_Achivment по его primary key (pk)
        achivement = get_object_or_404(Teacher_Achivment, pk=pk)
        # Удаляем найденный объект
        achivement.delete()
        return Response({'message': 'Achievement deleted successfully'}, status=204)
    
    


class AchivmentApiView(generics.ListAPIView):
    queryset = Achivment.objects.all()
    serializer_class = AchivmentSerializer

class Achivment_Category(generics.ListAPIView):
    queryset = Achivment_Category.objects.all()
    serializer_class = Achivment_CategorySerializer

class Score_Value(generics.ListAPIView):
    queryset = Score_Value.objects.all()
    serializer_class = Score_ValueSerializer

class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Теперь вы можете использовать объект пользователя (user) для доступа к его данным
        user_data = {
            'username': user.username,
            'email': user.email,
            'department': user.department_id_id,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'teacher': user.teacher_id_id
        }
        return Response(user_data)
