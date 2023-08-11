# Generated by Django 4.1.4 on 2023-02-09 11:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_candidatedetails_candidateworkexperience_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateResultIndividual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('answer_marks', models.FloatField()),
                ('candidate_answer', models.CharField(blank=True, max_length=500)),
                ('answer_status', models.CharField(choices=[('Correct', 'Correct'), ('Incorrect', 'Incorrect')], default='Incorrect', max_length=24)),
            ],
            options={
                'db_table': 'candidate_result_individual',
            },
        ),
        migrations.AddField(
            model_name='candidatedetails',
            name='district_permanent',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='candidatedetails',
            name='district_present',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='candidatedetails',
            name='profile_progress',
            field=models.CharField(default='Pending', max_length=100),
        ),
        migrations.AddField(
            model_name='candidatedetails',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='candidatesourceofinformation',
            name='consultancy',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='candidatesourceofinformation',
            name='newspaper',
            field=models.CharField(blank=True, choices=[('PATRIKA', 'Rajasthan Patrika'), ('BHASKAR', 'Dainik Bhaskar'), ('OTHER', 'Other')], max_length=100),
        ),
        migrations.AlterField(
            model_name='candidatedetails',
            name='mobile_no_2',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='candidateeducationdetails',
            name='board_university',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='candidateeducationdetails',
            name='division',
            field=models.CharField(blank=True, choices=[('1', 'First'), ('2', 'Second'), ('3', 'Third')], max_length=1),
        ),
        migrations.AlterField(
            model_name='candidateeducationdetails',
            name='education_details',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='candidateeducationdetails',
            name='medium',
            field=models.CharField(blank=True, choices=[('E', 'English'), ('H', 'Hindi'), ('O', 'Others')], max_length=1),
        ),
        migrations.AlterField(
            model_name='candidateeducationdetails',
            name='percentage',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='candidateeducationdetails',
            name='school_college',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='candidateeducationdetails',
            name='year_of_passing',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='candidatefamilydetails',
            name='dependent',
            field=models.BooleanField(blank=True),
        ),
        migrations.AlterField(
            model_name='candidatefamilydetails',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='candidatefamilydetails',
            name='occupation',
            field=models.CharField(blank=True, choices=[('BUSINESS', 'Business'), ('GOVT EMPLOYEE', 'Govt. Employee'), ('NOT EMPLOYED', 'Not Employed'), ('STUDENT', 'Student'), ('PVT EMPLOYEE', 'Private Employee'), ('HOUSEWIFE', 'Housewife')], max_length=100),
        ),
        migrations.AlterField(
            model_name='candidatefamilydetails',
            name='relation',
            field=models.CharField(blank=True, choices=[('FATHER', 'Father'), ('MOTHER', 'Mother'), ('BROTHER', 'Brother'), ('SISTER', 'Sister'), ('SPOUSE', 'Spouse')], max_length=7),
        ),
        migrations.AlterField(
            model_name='candidateotherdetails',
            name='salary_expected',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='candidatesourceofinformation',
            name='source_of_info',
            field=models.CharField(choices=[('CAMPUS', 'Arcgate Campus Drive'), ('WEBSITE', 'Arcgate Website'), ('EMPLOYEE', 'Arcgate Employee Referral'), ('FRIENDS', 'Friends/Family'), ('NEWSPAPER', 'Newspaper'), ('SOCIAL MEDIA', 'Arcgate Social Media'), ('WALK IN', 'Walk-In'), ('CONSULTANCY', 'Job Consultancy'), ('OTHER', 'Others')], max_length=500),
        ),
        migrations.AlterField(
            model_name='candidateworkexperience',
            name='last_salary',
            field=models.FloatField(null=True),
        ),
        migrations.CreateModel(
            name='CandidateResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.candidateresultindividual')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.grades')),
            ],
            options={
                'db_table': 'candidate_result',
            },
        ),
        migrations.AddField(
            model_name='candidateresultindividual',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.candidatedetails'),
        ),
        migrations.AddField(
            model_name='candidateresultindividual',
            name='paper_set_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.papersetupdescription'),
        ),
        migrations.AddField(
            model_name='candidateresultindividual',
            name='paper_subject_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.papersetupsubjectmap'),
        ),
        migrations.AddField(
            model_name='candidateresultindividual',
            name='subject_question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.subjectquestionmap'),
        ),
    ]