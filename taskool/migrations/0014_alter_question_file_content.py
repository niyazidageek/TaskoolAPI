# Generated by Django 4.0.2 on 2022-02-06 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskool', '0013_alter_question_file_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='file_content',
            field=models.ManyToManyField(to='taskool.File'),
        ),
    ]
