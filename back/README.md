# Документация API

## Модели

### Teacher
Модель представляет учителя.

Поля:
- `name` (CharField): Имя учителя.
- `surname` (CharField): Фамилия учителя.
- `parentName` (CharField): Отчество учителя.
- `department_id` (ForeignKey): Ссылка на кафедру, к которой принадлежит учитель.

### Department
Модель представляет кафедру.

Поля:
- `name` (CharField): Название кафедры.

### User
Расширение модели пользователя Django (`AbstractUser`) с добавлением поля `department_id`, которое ссылается на кафедру.

### Achivment_Category
Модель представляет категорию достижений.

Поля:
- `name` (CharField): Название категории.

### Achivment
Модель представляет достижение.

Поля:
- `name` (CharField): Название достижения.
- `achivments_category_id` (ForeignKey): Ссылка на категорию достижений, к которой принадлежит достижение.

### Teacher_Achivment
Модель, связывающая учителя и достижения.

Поля:
- `teacher_id` (ForeignKey): Ссылка на учителя.
- `Achivment` (ForeignKey): Ссылка на достижение.
- `score` (IntegerField): Оценка за достижение.

### Score_Value
Модель представляет значение баллов.

Поля:
- `score` (IntegerField): Значение баллов.
- `Achivment` (ForeignKey): Ссылка на достижение, к которому относится значение баллов.

## Представления

### TeacherApiView
Представление для получения списка учителей.

### DepartmentApiView
Представление для получения списка кафедр.

### DepartmentApiViewDetail
Представление для получения детальной информации о кафедре по ее ID.

### TeacherApiViewDetail
Представление для получения детальной информации об учителе по его ID.

### Teacher_AchivmentApiView
Представление для создания и получения списка достижений учителя.

### AchivmentApiView
Представление для получения списка достижений.

### Achivment_Category
Представление для получения списка категорий достижений.

### Score_Value
Представление для получения списка значений баллов.

### Logout
Представление для выхода из системы (удаление токена аутентификации).

### UserProfileView
Представление для получения профиля пользователя.

## URL-адреса

- `/api/v1/teachers/`: Список учителей.
- `/api/v1/departments/`: Список кафедр.
- `/api/v1/departments/<int:id>/`: Детальная информация о кафедре по ее ID.
- `/api/v1/teachers/<int:id>/`: Детальная информация об учителе по его ID.
- `/api/v1/achivments_category/`: Список категорий достижений.
- `/api/v1/achivments/`: Список достижений.
- `/api/v1/teacher_achivments/`: Создание и получение списка достижений учителя.
- `/api/v1/score_values/`: Список значений баллов.
- `/auth/`: URL-адреса для аутентификации.
- `/auth/token`: Получение токена аутентификации.
- `/logout/`: Выход из системы.
- `/profile/`: Профиль пользователя.

## Пример использования

```python
# Пример создания нового достижения для учителя
import requests

url = 'http://example.com/api/v1/teacher_achivments/'
data = {
    'teacher_id': 1,
    'Achivment': 1,
    'score': 80,
}
response = requests.post(url, data=data)
print(response.json())
```

## Зависимости у бэкенда
- django
- djangorestframework
- djoser
- django-cors-headers
