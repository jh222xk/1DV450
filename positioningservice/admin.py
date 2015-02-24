from django.contrib import admin
from .models import Position, Event, Tag, Coffee, Review


class PositionAdmin(admin.ModelAdmin):
    list_display = ('address', 'latitude', 'longitude')


class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('rating', 'description')


class EventAdmin(admin.ModelAdmin):
    list_display = ('position', 'user')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Position, PositionAdmin)
admin.site.register(Coffee, CoffeeAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Tag, TagAdmin)
