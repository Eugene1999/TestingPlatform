from django.contrib import admin

from .models import User
from tickets.models import TicketPassing


class PassingInline(admin.TabularInline):
    model = TicketPassing
    readonly_fields = ('passed_at', 'correct_answers_count',
                       'percent_of_passing')
    # can_delete = False
    extra = 0


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'birth_date', 'last_login')

    fieldsets = [
        ('General',               {'fields': [
         'username', 'password', 'is_staff', 'is_superuser']}),
        ('Profile', {'fields': ['first_name',
                                'last_name', 'avatar', 'birth_date', 'bio']}),
    ]
    inlines = [PassingInline]


admin.site.register(User, UserAdmin)
