from django.contrib import admin
from models import Owner
from models import ModelsLog


class OwnerAdmin(admin.ModelAdmin):
    pass


class ModelsLogAdmin(admin.ModelAdmin):
    pass

admin.site.register(Owner, OwnerAdmin)
admin.site.register(ModelsLog, ModelsLogAdmin)