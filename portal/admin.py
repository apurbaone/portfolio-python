from django.contrib import admin
from .models import Visitor, PortalPost

from django.contrib import admin as dj_admin

# Customize admin site header
dj_admin.site.site_header = 'Apurba.one administration'
dj_admin.site.site_title = 'Apurba.one admin'
dj_admin.site.index_title = 'Administration'


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip', 'path', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('ip', 'path', 'user_agent')


@admin.register(PortalPost)
class PortalPostAdmin(admin.ModelAdmin):
    list_display = ('post', 'visible')
    list_select_related = ('post',)
