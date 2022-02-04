from django.db import models
from django.utils.translation import gettext_lazy as _


def upload_to(instance, filename):
    return f'questions/{filename}'


class TimestampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Question(TimestampModel):
    name = models.CharField(max_length=255)
    point = models.FloatField()
    image = models.ImageField(_("Image"), upload_to=upload_to, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Option(TimestampModel):
    name = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class QuestionType(TimestampModel):
    name = models.CharField()


