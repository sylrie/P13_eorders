from django.contrib import admin
from .models import Comment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'date', 'visible')
    list_filter = ('visible', 'date')
    search_fields = ('user', 'message')
    actions = ['hide_comments']

    def approve_comments(self, request, queryset):
        queryset.update(visible=False)