# Generated by Django 5.0 on 2023-12-09 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gacha_app', '0002_school_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='version',
            field=models.CharField(default='Original', max_length=50),
        ),
    ]
