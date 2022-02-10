from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.v1.question.validator import question_file_validation


def upload_to(instance, filename):
    return f'questions/{filename}'


class TimestampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class File(TimestampModel):
    media = models.FileField(upload_to=upload_to, validators=question_file_validation)
    extension = models.CharField(max_length=20)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.media


class Question(TimestampModel):
    name = models.CharField(max_length=255)
    point = models.FloatField()
    file_content = models.ManyToManyField(File)
    is_option_based = models.BooleanField()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Option(TimestampModel):
    name = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    explanation = models.CharField(max_length=1000)
    file_content = models.ManyToManyField(File)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class TextAnswer(TimestampModel):
    text = models.CharField(max_length=2000)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.text


class AudioAnswer(TimestampModel):
    media = models.FileField(upload_to=upload_to, validators=question_file_validation)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.media


class Answer(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True)
    text_answer = models.OneToOneField(TextAnswer, on_delete=models.CASCADE, null=True)
    audio_answer = models.OneToOneField(AudioAnswer, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-id"]




