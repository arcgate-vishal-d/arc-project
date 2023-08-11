# Generated by Django 4.1.4 on 2023-01-20 05:36

import app.utility.question_module_functions
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_auto_20230106_0710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excelquestions',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, validators=[app.utility.question_module_functions.validate_check_null]),
        ),
        migrations.AlterField(
            model_name='excelquestions',
            name='description',
            field=models.CharField(max_length=500, validators=[app.utility.question_module_functions.validate_check_null]),
        ),
        migrations.AlterField(
            model_name='excelquestions',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.allquestions', validators=[app.utility.question_module_functions.validate_check_null]),
        ),
        migrations.AlterField(
            model_name='excelquestions',
            name='sheet_id',
            field=models.CharField(max_length=1000, validators=[app.utility.question_module_functions.validate_check_null]),
        ),
        migrations.AlterField(
            model_name='excelquestions',
            name='type',
            field=models.CharField(default='Excel', max_length=50, validators=[app.utility.question_module_functions.validate_check_null]),
        ),
        migrations.CreateModel(
            name='MultipleImageChoiceQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('question_title', models.CharField(max_length=1000)),
                ('answer_key', models.ImageField(upload_to='images/')),
                ('optionA', models.ImageField(upload_to='images/')),
                ('optionB', models.ImageField(upload_to='images/')),
                ('optionC', models.ImageField(upload_to='images/')),
                ('optionD', models.ImageField(upload_to='images/')),
                ('status', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.allquestions')),
            ],
            options={
                'db_table': 'multiple_image_choice_question',
            },
        ),
    ]