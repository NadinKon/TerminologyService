from django.contrib import admin
from .models import Refbook, RefbookVersion, RefbookElement


class RefbookElementInline(admin.TabularInline):
    model = RefbookElement
    extra = 1


class RefbookVersionInline(admin.TabularInline):
    model = RefbookVersion
    extra = 1
    show_change_link = True


@admin.register(Refbook)
class RefbookAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'current_version', 'current_version_start_date']
    inlines = [RefbookVersionInline]
    fields = ['code', 'name', 'description']

    def current_version(self, obj):
        latest_version = obj.versions.order_by('-start_date').first()
        return latest_version.version if latest_version else None
    current_version.short_description = 'Текущая версия'

    def current_version_start_date(self, obj):
        latest_version = obj.versions.order_by('-start_date').first()
        return latest_version.start_date if latest_version else None
    current_version_start_date.short_description = 'Дата начала действия версии'


@admin.register(RefbookVersion)
class RefbookVersionAdmin(admin.ModelAdmin):
    list_display = ['refbook_code', 'refbook_name', 'version', 'start_date']
    inlines = [RefbookElementInline]
    fields = ['refbook', 'version', 'start_date']

    def refbook_code(self, obj):
        return obj.refbook.code
    refbook_code.short_description = 'Код справочника'

    def refbook_name(self, obj):
        return obj.refbook.name
    refbook_name.short_description = 'Наименование справочника'


@admin.register(RefbookElement)
class RefbookElementAdmin(admin.ModelAdmin):
    list_display = ['version', 'code', 'value']
    fields = ['version', 'code', 'value']

