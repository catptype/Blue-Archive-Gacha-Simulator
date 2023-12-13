# Generated by Django 5.0 on 2023-12-13 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gacha_app', '0006_student_is_limited_alter_student_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='GachaBannerPreset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('rate_3_star', models.DecimalField(decimal_places=2, max_digits=5)),
                ('rate_2_star', models.DecimalField(decimal_places=2, max_digits=5)),
                ('rate_1_star', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.DeleteModel(
            name='Banner',
        ),
        migrations.AddField(
            model_name='school',
            name='member',
            field=models.ManyToManyField(related_name='members', to='gacha_app.student'),
        ),
    ]
