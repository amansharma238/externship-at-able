from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserChangeForm, MyUserCreationForm
from .models import SalesUser, Lead, Remark

# Register your models here.
admin.site.site_header = 'Leads Management Platform'


@admin.action(description='Mark selected Users as approved')
def make_approved(modeladmin, request, queryset):
    queryset.update(is_approved='True')


class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = SalesUser
    list_display = ['first_name', 'last_name', 'email',
                    'phone_number', 'is_staff', 'is_superuser', 'is_approved']

    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        ('Personal info', {'fields': ('first_name',
         'last_name', 'user_type', 'manager_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_approved'
                                    )}),
        ('Important dates', {
         'fields': ('last_login', 'date_joined')}),
        ('user_info', {'fields': ('phone_number',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number'),
        }),
    )

    search_fields = ('email',)
    ordering = ('created_at', )
    actions = [make_approved]


admin.site.register(SalesUser, MyUserAdmin)
admin.site.register(Lead)
admin.site.register(Remark)
