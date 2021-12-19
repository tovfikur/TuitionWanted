from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import GuardianDetails, Child, Note, ChildGroup, Post
# Register your models here.

admin.site.register(ChildGroup)
admin.site.register(Note)
admin.site.register(Post)


@admin.register(GuardianDetails)
class GuardianAdmin(admin.ModelAdmin):
    list_display = [
         'Name', 'id', 'Phone', 'Created'
    ]

    search_fields = ['id', 'Phone', 'Name', 'Child__slug']


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = [
        'slug', 'Name', 'Created', 'Reserved', 'Leads'
    ]
    list_filter = ['Created', 'Reserved', 'Leads', 'Paid', 'Canceled', 'active']
    list_editable = ['Reserved', 'Leads']
    search_fields = ['slug', 'Name', 'Phone', 'Address', 'Important_Note']

    fieldsets = (('Details', {
        'fields': ('Name', 'Phone', 'Address', 'Education_Level',
                   'Education_Institute', 'Education_Medium', 'Gender',
                   'Type', 'Paid', 'active', 'Canceled', 'Note', 'Free_Time', 'Free_Duration', 'Important_Note', 'Leads', 'Reserved',)
    }), ('Requirement', {
        'fields': ('Expected_Salary', 'PerClass', 'PerCourse', 'Expected_Day', 'Expected_Style', 'Expected_Subjects',
                   'Teacher_HSC_GOLD', 'Expected_School', 'Expected_College', 'Teacher_Gender', 'Teacher_Level',
                   'Teacher_Background', 'Teacher_Medium', 'Teacher_Type', 'Teacher_Experience', 'Teacher_Age',
                   'Teacher_University', 'Teacher_Religion')
    }), ('Guardian', {
        'fields': ('Guardian',)
    })
                 )


    actions = ['make_post', 'clear_leads', 'mark_leads']


    def clear_leads(self,  request, queryset):
        for i in queryset:
            i.Leads = False
            i.save()
            messages.add_message(request, messages.SUCCESS, i.slug + ' Leads cleared')

    def mark_leads(self,  request, queryset):
        for i in queryset:
            i.Leads = True
            i.save()
            messages.add_message(request, messages.INFO, i.slug + ' Marked for leads')

    def make_post(self, request, queryset):
        text = ''
        for i in queryset:
            text = text + str(i.gender_text()) + ' (' + str(i.t_university_text()) +','+str(i.background_text())+\
                   ','+str(i.experience_text())+') <br/>'
            text = text + 'Location: ' + str(i.address_text()) + '<br/>'
            text = text + 'Class: ' + str(i.level_text()) + '(' + str(i.teacher_medium_text()) + ')<br/>'
            text = text + 'Subject: ' + str(i.subject_text()) +'<br/>'
            text = text + 'Day: ' + str(i.Expected_Day) +'<br/>'
            text = text + 'Salary: ' + str(i.Expected_Salary) +'<br/>'
            text = text + 'CODE: ' + str(i.slug) +'<br/><br/>'

        messages.add_message(request, messages.INFO, mark_safe('<br/>'+text))
