# Generated by Django 4.0.4 on 2022-05-20 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='img_default.png', upload_to=''),
        ),
    ]
