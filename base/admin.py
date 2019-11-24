from django.contrib import admin
from base.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance',)
    ordering = ('balance', 'name',)
