# Generated by Django 5.1.5 on 2025-03-09 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachersRating', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_achievment',
            name='conference_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='employee_achievment',
            name='reciving_date',
            field=models.DateField(null=True),
        ),
    ]
