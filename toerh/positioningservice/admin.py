from django.contrib import admin
from .models import Position, Event, Tag


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude')


class EventAdmin(admin.ModelAdmin):
    list_display = ('position', 'user')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Position, PositionAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Tag, TagAdmin)
