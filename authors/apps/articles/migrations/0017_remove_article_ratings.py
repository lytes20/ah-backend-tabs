# Generated by Django 2.0.7 on 2018-08-06 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_article_ratings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='ratings',
        ),
    ]
