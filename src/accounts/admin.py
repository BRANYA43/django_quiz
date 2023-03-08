from django.contrib import admin
from django.utils.html import format_html

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_staff', 'is_active', 'is_activated')
    fieldsets = (
        (None, {'fields': (('avatar', 'avatar_img',), )}),
        ('Register info', {'fields': ('username', 'email')}),
        ('Personal info', {'fields': (('last_name', 'firts_name',), ('birthday', 'city',), )}),
        ('Permission', {'fields': ('groups', 'user_permissions')}),
        ('Flags', {'fields': (('is_superuser', 'is_staff', 'is_active', 'is_activated'), )}),
        (None, {'fields': (('last_login', 'date_joined'),)}),
    )
    readonly_fields = ('last_login', 'date_joined', 'avatar_img')

    def avatar_img(self, instance):
        return format_html(f'f<img scr="{instance.avatar.url}" alt="{instance.username}" width="50" height="50">')

    avatar_img.short_description = 'view'
