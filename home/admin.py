from django.contrib import admin
from .models import TempData

class TempDataAdmin(admin.ModelAdmin):
    list_display = (
        'set',
        'temperature',
        'x_point',
        'y_point'
    )

    ordering = ('set',)

admin.site.register(TempData, TempDataAdmin)

# Register your models here.
