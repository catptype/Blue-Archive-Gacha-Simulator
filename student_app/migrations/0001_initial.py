# Generated by Django 5.1.4 on 2025-01-10 15:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('school_id', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=100, unique=True, verbose_name='School')),
                ('school_image', models.BinaryField(null=True, verbose_name='Logo')),
            ],
            options={
                'db_table': 'student_school_table',
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('version_id', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_name', models.CharField(max_length=100, unique=True, verbose_name='Version')),
            ],
            options={
                'db_table': 'student_version_table',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=100)),
                ('student_rarity', models.PositiveIntegerField(choices=[(1, '★'), (2, '★★'), (3, '★★★')])),
                ('student_image', models.BinaryField(null=True, verbose_name='Portrait')),
                ('student_is_limited', models.BooleanField(default=False)),
                ('school_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app.school')),
                ('version_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app.version')),
            ],
            options={
                'db_table': 'student_table',
                'unique_together': {('student_name', 'version_id')},
            },
        ),
    ]
