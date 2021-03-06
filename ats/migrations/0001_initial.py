# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-26 00:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default=None, max_length=20, verbose_name='first name')),
                ('last_name', models.CharField(default=None, max_length=20, verbose_name='last name')),
                ('phone', models.CharField(default=None, max_length=15, verbose_name='phone')),
                ('email_address', models.EmailField(default=None, max_length=40, verbose_name='email')),
                ('zip_code', models.CharField(default=None, max_length=6, verbose_name='zip code')),
                ('source', models.CharField(choices=[('LIM', 'Linkedin Message'), ('REF', 'Referral'), ('NET', 'Networking Event'), ('LIP', 'Linkedin Posting'), ('CJP', 'Community Job Posting')], default=None, max_length=20, verbose_name='source')),
                ('linkedin', models.URLField(blank=True, default=None, null=True, verbose_name='linkedin')),
                ('resume', models.FileField(blank=True, default=None, null=True, upload_to='resumes/', verbose_name='resume')),
                ('writeup', models.TextField(blank=True, default=None, max_length=4000, null=True, verbose_name='writeup')),
                ('salary_base', models.IntegerField(blank=True, default=100, null=True, verbose_name='base')),
                ('salary_bonus', models.IntegerField(blank=True, default=20, null=True, verbose_name='bonus')),
                ('i9_status', models.CharField(choices=[('UNK', 'Unknown'), ('USC', 'US Citizen/Greencard'), ('H1B', 'H1B'), ('OPT', 'OPT')], default='UNK', max_length=3, null=True, verbose_name='i9 status')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('change_log', models.CharField(blank=True, max_length=4000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interview_type', models.CharField(choices=[('REVIEW', 'Submit/Review'), ('TECH_PHONE', 'Technical Phone'), ('TEST', 'Codetest'), ('ONSITE', 'Onsite'), ('INTRO', 'Intro Call'), ('HR', 'HR Call'), ('REJECT', 'Reject')], default='TECH_PHONE', max_length=11, null=True, verbose_name='interview type')),
                ('date_time', models.DateTimeField(blank=True, null=True, verbose_name='interview date/time')),
                ('outcome', models.CharField(choices=[('PASS', 'Pass'), ('FAIL', 'Fail'), ('NONE', 'Unknown')], default='NONE', max_length=5, verbose_name='interview type')),
                ('candidate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interviews_candidate', to='ats.Candidate')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=10000)),
                ('currently_open', models.BooleanField(default=False)),
                ('company', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkedin', models.CharField(default=None, max_length=40, verbose_name='Linkedin')),
                ('phone', models.CharField(default=None, max_length=15, verbose_name='phone')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TagType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('LANG', 'Language'), ('DB', 'Database'), ('FUNC', 'Function'), ('TECH', 'Technology'), ('MISC', 'Miscellaneous')], default=None, max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='tagtype',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='tag_TagType', to='ats.TagType'),
        ),
        migrations.AddField(
            model_name='job',
            name='tags',
            field=models.ManyToManyField(to='ats.Tag'),
        ),
        migrations.AddField(
            model_name='interview',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interviews_job', to='ats.Job'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='jobs',
            field=models.ManyToManyField(blank=True, to='ats.Job'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='recruiter',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ats.Recruiter'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='tags',
            field=models.ManyToManyField(default=None, to='ats.Tag'),
        ),
    ]
