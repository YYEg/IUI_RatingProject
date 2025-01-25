from django.contrib import admin



from .models import Teacher, Department, Teacher_Achivment, Achivment, Achivment_Category
from .models import User


admin.site.register(Teacher)
admin.site.register(Department)
admin.site.register(Teacher_Achivment)
admin.site.register(Achivment)
admin.site.register(Achivment_Category)
admin.site.register(User)