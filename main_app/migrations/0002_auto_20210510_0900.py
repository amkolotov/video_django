# Generated by Django 3.2.2 on 2021-05-10 09:00

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='preview',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to=main_app.models.file_name, verbose_name='Видео'),
        ),
    ]
