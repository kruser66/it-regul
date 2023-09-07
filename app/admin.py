from django.contrib import admin
from app.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    pass
