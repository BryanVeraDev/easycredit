from __future__ import unicode_literals

import copy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from authtools.forms import UserChangeForm
from .models import User

USERNAME_FIELD = get_user_model().USERNAME_FIELD

REQUIRED_FIELDS = (USERNAME_FIELD,) + tuple(get_user_model().REQUIRED_FIELDS)

BASE_FIELDS = (None, {
    'fields': REQUIRED_FIELDS + ('password',),
})

SIMPLE_PERMISSION_FIELDS = (_('Permissions'), {
    'fields': ('is_active', 'is_staff', 'is_superuser',),
})

ADVANCED_PERMISSION_FIELDS = copy.deepcopy(SIMPLE_PERMISSION_FIELDS)
ADVANCED_PERMISSION_FIELDS[1]['fields'] += ('groups',)

DATE_FIELDS = (_('Important dates'), {
    'fields': ('last_login', 'date_joined',),
})

class UserAdmin(DjangoUserAdmin):
    add_form_template = None
    add_form = UserCreationForm
    form = UserChangeForm
    
    list_display = ('is_active', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'last_login', 'date_joined')
    list_display_links = ('email', 'first_name', 'last_name')
    fieldsets = (
        BASE_FIELDS,
        ADVANCED_PERMISSION_FIELDS,
    )
    add_fieldsets = (
        (None, {
            'fields': REQUIRED_FIELDS + (
                'password1',
                'password2',
            ),
        }),
        ADVANCED_PERMISSION_FIELDS,
    )
    
    search_fields = ('email', 'first_name')
    ordering = None
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_login', 'date_joined')
    
admin.site.register(User, UserAdmin)
