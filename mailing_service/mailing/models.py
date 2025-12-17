from django.db import models

class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=100, verbose_name='Ф.И.О.')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return self.email

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


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(blank=True, verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f"Попытка {self.id} ({self.status})"
