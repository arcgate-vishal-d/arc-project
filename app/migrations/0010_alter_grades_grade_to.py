# Generated by Django 4.1.4 on 2023-04-04 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_candidateeducationdetails_qualifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grades',
            name='grade_to',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
