from django.db import models
from application.settings import AUTH_USER_MODEL
from users.models import User
from chats.models import Chat

# Create your models here.


class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='chat_messages',
        verbose_name='Чат'
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Отправлено в'
    )
    sender = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sender_messages',
        verbose_name='Отправитель сообщения'
    )
    content = models.TextField(
        verbose_name='Содержание сообщения'
    )
    is_readed = models.BooleanField(
        default=False,
        verbose_name='Прочитано сообщение'
    )
    is_editing = models.BooleanField(
        default=False,
        verbose_name='Отредактировано сообщение'
    )

    def __str__(self):
        return f'Сообщение пользователя {self.sender} в чате {self.chat_id}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Reaction(models.Model):
    kind = models.CharField(   
        max_length=30,
        verbose_name='Вид реакции'
    )

    def __str__(self):
        return self.kind

    class Meta:
        verbose_name = 'Реакция'
        verbose_name_plural = 'Реакции'


class UserReaction(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='message_userreactions',
        verbose_name='Сообщение'
    )
    reaction = models.ForeignKey(
        Reaction,
        on_delete=models.CASCADE,
        related_name='reaction_userreactions',
        verbose_name='Реакция',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_userreactions',
        null=True,
        blank=True
    )
    time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.user} поставил реакцию {self.reaction}'

    class Meta:
        verbose_name = 'Реакция пользователей'
        verbose_name_plural = 'Реакции пользователей'
