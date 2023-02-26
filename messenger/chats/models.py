from django.db import models
from application.settings import AUTH_USER_MODEL

# Create your models here.


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название категории'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Chat(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название чата'
    )
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Описание чата'
    )
    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_chats',
        verbose_name='Создатель чата'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category_chats',
        verbose_name='Категория чата'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан в'
    )
    avatar = models.ImageField(  
        upload_to=('static/'),
        blank=True,
        null=True,
        verbose_name='Аватар чата'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class ChatMember(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_chatmembers'
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        verbose_name='Чат',
        related_name='chat_chatmembers'
    )
    is_admin = models.BooleanField(
        verbose_name='Администратор',
        default=False
    )
    adding_time = models.DateTimeField(  
        auto_now_add=True,
        verbose_name='Время добавления'
    )

    def __str__(self):
        return f'{self.user} из {self.chat}'

    class Meta:
        verbose_name = 'Участник чата'
        verbose_name_plural = 'Участники чата'
