from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Table)
admin.site.register(TableConnect)
admin.site.register(Payment)
admin.site.register(Call)

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_filter = ('table', 'status')

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_filter = ('status', 'date', 'bill')
    actions = ['change_to_delivered']

    def mark_delivered(self, request, queryset):
        queryset.update(status="delivered")