# Generated by Django 4.0.2 on 2022-02-04 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskool', '0007_question_files_delete_questionfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='files',
        ),
    ]
