from django.contrib import admin
from .models import ChatHistory

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'timestamp')
    search_fields = ('user__username', 'query', 'response')
    list_filter = ('timestamp', 'user')
