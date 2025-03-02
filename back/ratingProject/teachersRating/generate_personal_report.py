from openpyxl import Workbook
from openpyxl.styles import Font

def generate_personal_report(request):
    # Создаем новый Excel-документ
    wb = Workbook()
    ws = wb.active
    ws.title = "Шаблон достижений"

    # Заголовки
    ws.append(["№ п/п", "Наименование показателя", "Единица измерения", "Баллы за показатель", "Подтверждающие документы", "Количество баллов"])

    # Получаем данные из базы данных (заглушка)
    groups = [
        {"id": 1, "name": "Группа 1", "description": "Описание группы 1"},
        {"id": 2, "name": "Группа 2", "description": "Описание группы 2"},
    ]

    achievements = [
        {"id": 1, "name": "1.1 Выполнение объема контактной работы", "group_id": 1, "meas_unit": "часы", "meas_unit_score": 30},
        {"id": 2, "name": "1.2 Руководство выпускной квалификационной работой", "group_id": 1, "meas_unit": "шт.", "meas_unit_score": 10},
        {"id": 3, "name": "2.1 Шляпных дел мастер", "group_id": 2, "meas_unit": "шт.", "meas_unit_score": 10},
    ]

    # Заполняем группы и достижения
    row_num = 2
    for group in groups:
        ws.append([f"Группа {group['id']}", group["name"], "", "", "", ""])
        ws[f"A{row_num}"].font = Font(bold=True)
        row_num += 1

        for achievement in achievements:
            if achievement["group_id"] == group["id"]:
                ws.append(["", achievement["name"], achievement["meas_unit"], achievement["meas_unit_score"], "", ""])
                row_num += 1

    # Сохраняем документ
    wb.save("achievements_template.xlsx")