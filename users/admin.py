from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User,userCode




@admin.register(userCode)
class usercodeAdmin(admin.ModelAdmin):
    list_display = ('code',)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id","name", "phone","created", "modified")
    list_filter = ("is_active", "is_staff", "groups")
    search_fields = ("name",)
    ordering = ("name",)
 

    fieldsets = (
        (None, {"fields": ("phone","name", "img","password","age","location","temp_phone")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "socialconnected","sociallogin","is_staff", "is_superuser", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("phone", "password1", "password2")}),)
