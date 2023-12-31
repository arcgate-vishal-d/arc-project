# Generated by Django 4.1.4 on 2023-02-08 09:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_excelquestions_screenshot_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='excelquestions',
            name='screenshot_date',
        ),
        migrations.AddField(
            model_name='excelquestions',
            name='excel_last_edited',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='excelquestions',
            name='screenshot',
            field=models.ImageField(blank=True, upload_to='excel_screenshots/'),
        ),
    ]
