# Generated by Django 4.0.3 on 2023-01-18 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FaceApp', '0004_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.FileField(upload_to='faces'),
        ),
    ]
