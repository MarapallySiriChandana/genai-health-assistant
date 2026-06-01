from django.contrib import admin
from .models import ImageAnalysis

@admin.register(ImageAnalysis)
class ImageAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp')
    search_fields = ('user__username', 'analysis_result')
    list_filter = ('timestamp',)
