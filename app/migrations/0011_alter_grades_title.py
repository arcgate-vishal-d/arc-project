# Generated by Django 4.1.4 on 2023-05-23 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_grades_grade_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grades',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]