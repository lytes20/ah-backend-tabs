# Generated by Django 2.0.7 on 2018-08-06 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20180806_1632'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='article',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='ratings',
            field=models.IntegerField(default=0),
        ),
    ]
