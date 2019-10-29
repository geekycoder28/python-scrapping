from django.contrib import admin
from .models import User


class BurstoutUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, BurstoutUserAdmin)
