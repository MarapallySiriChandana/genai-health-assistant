from django.contrib import admin
from .models import SymptomPrediction

@admin.register(SymptomPrediction)
class SymptomPredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'predicted_disease', 'confidence', 'timestamp')
    search_fields = ('user__username', 'predicted_disease')
    list_filter = ('timestamp', 'predicted_disease')
