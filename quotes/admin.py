from django.contrib import admin
from .models import Source, Quote


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'year', 'created_at']
    list_filter = ['type', 'year']
    search_fields = ['title']


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text_short', 'source', 'weight', 'views_count', 'likes', 'dislikes']
    list_filter = ['source', 'created_at']
    search_fields = ['text', 'source__title']

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_short.short_description = 'Текст'