from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Task(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(max_length=255, null=True, blank=True, verbose_name='Описание')
    due_date = models.DateField(verbose_name='Установленный срок')
    due_time = models.TimeField(verbose_name='Установленное время')
    work = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.title}'

    class Meta:
        verbose_name = 'Задачу'
        verbose_name_plural = 'Задачи'