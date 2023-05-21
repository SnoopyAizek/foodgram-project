from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Subscribe, User


@register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('pk', 'username', 'email', 'password',
                    'first_name', 'last_name', 'is_active')
    list_editable = ('password',)
    list_filter = ('username', 'email')
    search_fields = ('username', 'email',)
    save_on_top = True


@register(Subscribe)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'following')
    list_editable = ('author', 'following')
    empty_value_display = 'Данных нет'
