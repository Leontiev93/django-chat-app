from django.db import models
from django.conf import settings


class Conversation(models.Model):
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name="convo_starter"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="convo_participant"
    )
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.initiator} пригласил в беседу {self.receiver} начата в {self.start_time}'


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='message_sender')
    text = models.CharField(
        max_length=200,
        blank=True)
    attachment = models.FileField(blank=True)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self) -> str:
        return self.text
