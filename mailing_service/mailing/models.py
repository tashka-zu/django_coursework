from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def get_default_owner():
    user = User.objects.filter(is_superuser=True).first()
    return user.id

class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=100, verbose_name='Ф.И.О.')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return self.email

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        default=get_default_owner  # Значение по умолчанию
    )

class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Дата и время первой отправки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Создана', verbose_name='Статус')
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField('Client', verbose_name='Получатели')

    def __str__(self):
        return f"Рассылка {self.id} ({self.status})"

    def get_statistics(self):
        attempts = self.mailingattempt_set.all()
        success_count = attempts.filter(status='success').count()
        failed_count = attempts.filter(status='failed').count()
        return {
            'success_count': success_count,
            'failed_count': failed_count,
            'total_attempts': attempts.count(),
        }

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        default=get_default_owner  # Значение по умолчанию
    )

    class Meta:
        permissions = [
            ('can_view_all_mailings', 'Может просматривать все рассылки'),
            ('can_disable_mailings', 'Может отключать рассылки'),
        ]


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
