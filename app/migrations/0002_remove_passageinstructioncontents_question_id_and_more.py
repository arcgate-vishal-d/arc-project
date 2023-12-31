# Generated by Django 4.1.4 on 2023-01-06 07:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passageinstructioncontents',
            name='question_id',
        ),
        migrations.AddField(
            model_name='subjectivequestions',
            name='instructions',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.CreateModel(
            name='PaperSetupPassageMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('paper_setup_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.papersetupdescription')),
                ('passage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.passageinstructioncontents')),
            ],
            options={
                'db_table': 'paper_setup_passage_map',
            },
        ),
    ]
