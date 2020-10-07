from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'date', 'visible')
    list_filter = ('visible', 'date')
    search_fields = ('user', 'message')
    