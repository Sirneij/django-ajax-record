from django.contrib import admin

from core.models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("id", "language", "voice_record")
