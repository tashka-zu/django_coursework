from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def get_default_owner():
    user = User.objects.filter(is_superuser=True).first()
    if user is None:
        return None
    return user.id

class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        null=True,
        blank=True,
        default=get_default_owner
    )

    def __str__(self):
        return f"{self.full_name} ({self.email})"

class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название рассылки', null=True, blank=True)
    clients = models.ManyToManyField('Client', verbose_name='Клиенты')
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='Сообщение')
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    PERIOD_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]
    periodicity = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES,
        verbose_name='Периодичность',
        default='daily'
    )
    status = models.CharField(max_length=20, default='created', verbose_name='Статус')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        null=True,
        blank=True,
        default=None
    )

    def __str__(self):
        return self.name

class MailingAttempt(models.Model):
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, verbose_name='Рассылка')
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Время попытки')
    status = models.CharField(max_length=20, choices=[
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ], verbose_name='Статус')
    server_response = models.TextField(blank=True, null=True, verbose_name='Ответ сервера')

    def __str__(self):
        return f"Попытка {self.mailing} - {self.status}"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
