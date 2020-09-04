from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(ProductFamily)
admin.site.register(ProductCategory)
admin.site.register(ProductTaxe)
admin.site.register(StaffCall)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('avaiable', 'category', 'family')

