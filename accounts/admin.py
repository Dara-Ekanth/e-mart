from django.contrib import admin
from .models import CustomUser
from .form import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Info',
            {
                'fields': (
                    'Birthday',
                    'phone_number',
                    'Gender',
                    'address1',
                    'address2',
                    'pin_code',
                    'city',
                    'country',
                    'profile_pic',
                    'proof'
                )
            }
        )
    )


admin.site.register(CustomUser, CustomUserAdmin)
