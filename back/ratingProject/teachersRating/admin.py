from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from .models import Employee, Department, EmployeeAchievment, Achievment, User, AchievmentGroup, PubGrief, PubLevel, PubType, AchievmentType

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(EmployeeAchievment)
admin.site.register(Achievment)
admin.site.register(AchievmentGroup)
admin.site.register(PubType)
admin.site.register(PubGrief)
admin.site.register(PubLevel)
admin.site.register(AchievmentType)

User = get_user_model()
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'employee', 'department', 'role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('employee', 'department', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('employee', 'department', 'role')}),
    )

    def save_model(self, request, obj, form, change):
        # Проверяем, был ли изменен пароль и он не захеширован
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)  # Хешируем пароль
        super().save_model(request, obj, form, change)

# Регистрируем кастомную модель пользователя в админке
admin.site.register(User, CustomUserAdmin)