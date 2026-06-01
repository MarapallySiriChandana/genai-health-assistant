from django.contrib import admin
from .models import DrugInfo

@admin.register(DrugInfo)
class DrugInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'dosage')
    search_fields = ('name', 'usage', 'side_effects')
