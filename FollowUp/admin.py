from django.contrib import admin
from .models import TemporaryTuitionForChild, PermanentTuitionForChild, \
    TeacherHistory, GuardianHistory, User, ShortListedTuitionForChild, \
    AssignedTeacherForChild, SMS, EmployeeLoginHistory, Reminder, DemoTeacherForChild, RoughNote
from django.contrib.admin.models import LogEntry
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class TeacherListAdmin(admin.ModelAdmin):
    list_display = ['Child_id',]
    search_fields = ['Child_id']

admin.site.register(TemporaryTuitionForChild, TeacherListAdmin)
admin.site.register(PermanentTuitionForChild,TeacherListAdmin )
admin.site.register(TeacherHistory)
admin.site.register(GuardianHistory)
admin.site.register(ShortListedTuitionForChild, TeacherListAdmin)
admin.site.register(AssignedTeacherForChild, TeacherListAdmin)
admin.site.register(DemoTeacherForChild, TeacherListAdmin)

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Role',
            {
                'fields': (
                    'is_Checker',
                    'is_FollowUpper',
                    'is_Reserves',
                    'is_OfferCatcher',
                    'is_Guardian',
                    'is_Teacher',
                    'Job_Title',
                    'Job_Shift',
                )

            }
        ),
        (
            'Files',
            {
                'fields': (
                    'Phone_Number',
                    'Avatar',
                    'NID',
                    'Proof_Of_Presence'
                )
            }
        ),
        (
            'Connection',
            {
                'fields': (
                    'Guardian',
                    'Teacher'
                )
            }
        )
    )


admin.site.register(User, CustomUserAdmin)

# Administration entry
admin.site.register(LogEntry)


@admin.register(SMS)
class SMSAdmin(admin.ModelAdmin):
    list_display = ['sender', 'number', 'text']
    readonly_fields = ['sender', 'number', 'text']


@admin.register(EmployeeLoginHistory)
class SMSAdmin(admin.ModelAdmin):
    list_display = ['User', 'Date', 'Login', 'Logout']

    readonly_fields = ['User', 'Date', 'Login', 'Logout']
    list_filter = ['Date', 'User', ]


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['User', 'Time', 'Note', ]


@admin.register(RoughNote)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['user', 'Child', 'Text', 'time']

    search_fields = ['Child__Name', 'Child__slug', 'Child__slug', 'Child__Important_Note']
