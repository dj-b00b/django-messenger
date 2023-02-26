from ipaddress import ip_address
from django.db import models
from django.contrib.auth.models import AbstractUser
from application.settings import AUTH_USER_MODEL
from django.contrib.sessions.models import Session

# Create your models here.


class UserSession(Session):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    name_device = models.CharField(
        max_length=25,
        verbose_name='Название устройства'
    )
    latest_activity = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Последняя активность'
    )
    geolocation = models.CharField(
        max_length=25,
        verbose_name='Местоположение устройства'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='IP-адрес устройства'
    )
    is_active = models.BooleanField(
        verbose_name='Активна сессия',
        default=True
    )

    def __str__(self):
        return f'Сессия пользователя {self.user}'


class User(AbstractUser):
    about_user = models.CharField(
        max_length=70,
        verbose_name='Информация о пользователе',
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name='Номер телефона'
    )
    avatar = models.ImageField(  
        upload_to=('static/'),
        blank=True,
        null=True,
        verbose_name='Аватар пользователя'
    )


class Contact(models.Model): 
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь, добавляющий контакт',
        related_name='user_contacts' 
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Имя'
    )
    surname = models.CharField(
        max_length=255,
        verbose_name='Фамилия',
        blank=True,
        null=True
    )
    phone_number = models.CharField(  
        max_length=15,
        verbose_name='Номер телефона'
    )
    friend = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Добавляемый в контакты пользователь', 
        related_name='friend_contacts'
    )

    def __str__(self):
        return f'{self.friend} в контактах у {self.user}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
