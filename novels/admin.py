from django.contrib import admin
from .models import Novel, Chapter, Category, ReadingHistory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'author_name', 'category', 'status', 'views', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'author__username', 'author_name')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'novel', 'chapter_number', 'views', 'created_at', 'author_text')
    list_filter = ('created_at',)
    search_fields = ('title', 'novel__title', 'author_text')
    raw_id_fields = ['novel']
    date_hierarchy = 'created_at'

@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter', 'last_read')
    list_filter = ('last_read',)
    search_fields = ('user__username', 'chapter__title')