# Generated by Django 2.2.4 on 2020-01-27 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_question_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_desc',
            field=models.CharField(default='', max_length=200),
        ),
    ]
