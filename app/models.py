from django_prometheus.models import ExportModelOperationsMixin

from django.contrib.auth.models import User
from django.db import models


class Topic(ExportModelOperationsMixin("topic"), models.Model):
    """
    Модель тем сообщений
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(ExportModelOperationsMixin("room"), models.Model):
    """
    Модель комнат
    """

    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]  # sort value in template

    def __str__(self):
        return self.name


class Message(ExportModelOperationsMixin("message"), models.Model):
    """
    Модель сообщений на форуме
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]  # sort value in template

    def __str__(self):
        return self.body[:50]
