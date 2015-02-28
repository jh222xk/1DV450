from django.contrib import admin

from .models import Position, Tag, Coffee, Review


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('address', 'latitude', 'longitude')


@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('rating', 'description')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

