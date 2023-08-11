# Generated by Django 4.1.4 on 2023-01-24 13:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_excelquestions_screenshot_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('dob', models.DateField()),
                ('mobile_no_1', models.BigIntegerField()),
                ('mobile_no_2', models.BigIntegerField(null=True)),
                ('present_address', models.CharField(max_length=200)),
                ('permanent_address', models.CharField(max_length=200)),
                ('test_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.testlevels')),
            ],
            options={
                'db_table': 'candidate_details',
            },
        ),
        migrations.CreateModel(
            name='CandidateWorkExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name_of_company', models.CharField(max_length=100, null=True)),
                ('designation', models.CharField(max_length=100, null=True)),
                ('joining_date', models.DateField(null=True)),
                ('reliving_date', models.DateField(null=True)),
                ('reason_of_leaving', models.CharField(max_length=500, null=True)),
                ('last_salary', models.IntegerField(null=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.candidatedetails')),
            ],
            options={
                'db_table': 'candidate_work_experience',
            },
        ),
        migrations.CreateModel(
            name='CandidateSourceOfInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('previous_interviewed', models.BooleanField(default=False)),
                ('previous_worked', models.BooleanField(default=False)),
                ('source_of_info', models.CharField(choices=[('CAMPUS', 'Arcgate Campus Drive'), ('WEBSITE', 'Arcgate Website'), ('EMPLOYEE', 'Arcgate Employee'), ('FRIENDS', 'Friends'), ('NEWSPAPER', 'Newspaper'), ('OTHER', 'Others')], max_length=9)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.candidatedetails')),
            ],
            options={
                'db_table': 'source_of_information',
            },
        ),
        migrations.CreateModel(
            name='CandidateOtherDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('service_commitment', models.BooleanField()),
                ('salary_security', models.BooleanField()),
                ('shift', models.CharField(choices=[('D', 'Day'), ('N', 'Night'), ('A', 'Any')], max_length=1)),
                ('expected_joining_date', models.DateField()),
                ('salary_expected', models.IntegerField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.candidatedetails')),
            ],
            options={
                'db_table': 'other_details',
            },
        ),
        migrations.CreateModel(
            name='CandidateFamilyDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('relation', models.CharField(choices=[('FATHER', 'Father'), ('MOTHER', 'Mother'), ('BROTHER', 'Brother'), ('SISTER', 'Sister'), ('SPOUSE', 'Spouse')], max_length=7)),
                ('occupation', models.CharField(max_length=100)),
                ('dependent', models.BooleanField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.candidatedetails')),
            ],
            options={
                'db_table': 'candidate_family_details',
            },
        ),
        migrations.CreateModel(
            name='CandidateEducationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('qualifications', models.CharField(choices=[('ADDITIONAL_QUALIFICATION', 'Additional Qualification'), ('PG', 'Post Graduate'), ('UG', 'Under Graduate'), ('DIPLOMA', 'Diploma'), ('12', 'Higher Secondary'), ('10', 'Secondary')], max_length=24, null=True)),
                ('education_details', models.CharField(max_length=500)),
                ('school_college', models.CharField(max_length=100)),
                ('board_university', models.CharField(max_length=100)),
                ('year_of_passing', models.IntegerField()),
                ('division', models.CharField(choices=[('1', 'First'), ('2', 'Second'), ('3', 'Third')], max_length=1)),
                ('percentage', models.FloatField()),
                ('medium', models.CharField(choices=[('E', 'English'), ('H', 'Hindi'), ('O', 'Others')], max_length=1)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.candidatedetails')),
            ],
            options={
                'db_table': 'education_details',
            },
        ),
    ]