# Generated by Django 3.1 on 2020-10-03 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0013_auto_20201003_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='likes_num',
            field=models.PositiveIntegerField(default=0, verbose_name='点赞数'),
        ),
    ]
