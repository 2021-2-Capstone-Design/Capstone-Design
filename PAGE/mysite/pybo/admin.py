from django.contrib import admin

# Register your models here.
from .models import *


class TeamAdmin(admin.ModelAdmin):
    search_fields = ['teamName']


#
#
# admin.site.register(Team, TeamAdmin)
# admin.site.register(TeamMember)
