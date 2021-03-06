# Generated by Django 3.1.7 on 2021-06-08 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_username'),
        ('blog', '0002_auto_20210606_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='views',
            field=models.ManyToManyField(related_name='views', to='user.User'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to='user.User'),
        ),
    ]
