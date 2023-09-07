from django.db import models


class TgUser(models.Model):
    telegram_id = models.IntegerField('Телеграм ID пользователя', unique=True)
    phone = models.CharField('Мобильный телефон', max_length=12, blank=True)
    firstname = models.CharField('Имя пользователя', max_length=50, blank=True)
    lastname = models.CharField('Фамилия пользователя', max_length=100, blank=True)
    username = models.CharField('Телеграм username', max_length=150, blank=True)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return f'{self.firstname} {self.lastname}, телефон: {self.phone}'
