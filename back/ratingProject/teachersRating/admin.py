from django.contrib import admin



from .models import Employee, Department, Employee_Achievment, Achievment
from .models import User


admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Employee_Achievment)
admin.site.register(Achievment)
admin.site.register(User)