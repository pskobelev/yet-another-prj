from django.contrib import admin  # type: ignore

from app.models import Room, Message, Topic


# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass
