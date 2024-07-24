from django.contrib import admin

from charity.models import Institution


# Register your models here.
@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    search_fields = ('name', 'type')
    list_filter = ('type', 'categories')
    filter_horizontal = ('categories',)
