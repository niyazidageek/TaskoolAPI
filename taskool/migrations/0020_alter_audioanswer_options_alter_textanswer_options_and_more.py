# Generated by Django 4.0.2 on 2022-02-08 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskool', '0019_alter_answer_options_alter_audioanswer_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='audioanswer',
            options={},
        ),
        migrations.AlterModelOptions(
            name='textanswer',
            options={},
        ),
        migrations.RemoveField(
            model_name='audioanswer',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='textanswer',
            name='answer',
        ),
        migrations.AddField(
            model_name='answer',
            name='audio_answer',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='taskool.audioanswer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='answer',
            name='text_answer',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='taskool.textanswer'),
            preserve_default=False,
        ),
    ]
