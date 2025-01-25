from django.test import TestCase
from teachersRating.models import Teacher_Achivment, Teacher, Achivment, Department, Achivment_Category

class TeacherAchivmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        department = Department.objects.create(name='Test Department')
        teacher = Teacher.objects.create(name='Test', surname='Teacher', parentName='Parent', department_id=department)
        achivment_category = Achivment_Category.objects.create(name='Test Category')
        achivment = Achivment.objects.create(name='Test Achivment', achivments_category_id=achivment_category)
        Teacher_Achivment.objects.create(teacher_id=teacher, Achivment=achivment, score=50)

    def test_teacher_achivment_teacher_id(self):
        achivment = Teacher_Achivment.objects.get(id=1)
        field_label = achivment._meta.get_field('teacher_id').verbose_name
        self.assertEqual(field_label, 'teacher id')

    def test_teacher_achivment_Achivment(self):
        achivment = Teacher_Achivment.objects.get(id=1)
        field_label = achivment._meta.get_field('Achivment').verbose_name
        self.assertEqual(field_label, 'Achivment')

    def test_teacher_achivment_score(self):
        achivment = Teacher_Achivment.objects.get(id=1)
        field_label = achivment._meta.get_field('score').verbose_name
        self.assertEqual(field_label, 'score')

    def test_teacher_achivment_teacher_id_null(self):
        achivment = Teacher_Achivment.objects.get(id=1)
        field_null = achivment._meta.get_field('teacher_id').null
        self.assertFalse(field_null)

    def test_teacher_achivment_Achivment_null(self):
        achivment = Teacher_Achivment.objects.get(id=1)
        field_null = achivment._meta.get_field('Achivment').null
        self.assertFalse(field_null)

    def test_teacher_achivment_score_default(self):
        achivment = Teacher_Achivment.objects.get(id=1)
        default_value = achivment._meta.get_field('score').default
        self.assertEqual(default_value, 0)
