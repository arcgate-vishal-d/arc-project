# Generated by Django 4.1.4 on 2023-02-24 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_candidateresultindividual_paper_set_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidatedetails',
            name='sheet_id',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
    ]