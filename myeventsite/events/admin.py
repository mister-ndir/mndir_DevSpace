from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_featured')
    list_filter = ('is_featured', 'date', 'location')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    ordering = ('-date',)
