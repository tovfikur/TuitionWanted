from django.contrib import admin
from .models import Teacher, University, Schools, Subject, TeachingSection, Areas, SSC_HSC_Group, District, Division, Thana,\
    ClassesSubject
from FollowUp.models import Child, TemporaryTuitionForChild
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


# Register your models here.

admin.site.register(SSC_HSC_Group)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'SHORT', 'Category']
    search_fields = ['id', 'Name', 'SHORT', 'Category']
    list_filter = ['Name', 'SHORT', 'Category']


@admin.register(Schools)
class SchoolsAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'SHORT']
    search_fields = ['id', 'Name', 'SHORT']
    list_filter = ['Name', 'SHORT']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'Title', 'SHORT']
    search_fields = ['id', 'Title', 'SHORT']
    list_filter = ['Title', 'SHORT']


admin.site.register(TeachingSection)


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


@admin.action(description='Send reserve')
def set_teacher(self, request, queryset):
    for i in queryset:
        try:
            if request.session['child_id']:
                temp_obj = TemporaryTuitionForChild.objects.get(Child__slug=request.session['child_id'])
                temp_obj.Teacher.add(i)
                messages.add_message(request, messages.INFO, str(i.id) + 'Added to ' + request.session['child_id'])
            else:
                messages.add_message(request, messages.INFO, 'No child selected')
        except:
            if request.session['child_id']:
                c_obj = Child.objects.get(slug=request.session['child_id'])
                temp_obj = TemporaryTuitionForChild(Child=c_obj)
                temp_obj.save()
                temp_obj.Teacher.add(i)
                temp_obj.save()
                messages.add_message(request, messages.INFO, str(i.id) + 'Added to ' + request.session['child_id'])
            else:
                messages.add_message(request, messages.INFO, 'No child selected')
        # messages.add_message(request, messages.INFO, str(i.id) + 'Added to ' + request.session['child_id'])


# #
# @admin.action(description='set hsc ssc null')
# def set_ssc(self, request, queryset):
#     for i in Teacher.objects.all():
#         i.delete()


@admin.action(description='See requirements')
def see_requirements(self, request, queryset):
    for i in queryset:
        try:
            if request.session['child_id']:
                temp_obj = Child.objects.get(slug=request.session['child_id'])
                medium = str(temp_obj.medium_text())
                gender = str(temp_obj.gender_text())
                subjects = ''
                for i in temp_obj.Expected_Subjects.all():
                    subjects = subjects + i.SHORT + ', '
                background = str(temp_obj.background_text())
                university = str(temp_obj.teacher_university_text())
                experience = str(temp_obj.experience_text())
                expected = str(temp_obj.Expected_Salary)
                style = str(temp_obj.style_text())
                type = str(temp_obj.teacher_type_text())
                age = str(temp_obj.teacher_age_text())
                religion = str(temp_obj.teacher_religion_text())
                free = temp_obj.Free_Time
                string = """medium: """ + medium + """, 
                <br> gender: """ + gender + """, 
               <br> subject: """ + subjects + """, 
                <br>background: """ + background + """ ,
                 <br>university: """ + university + """, 
                 <br>experience: """ + experience + """, 
                 <br>salary: """ + expected + """, 
                 <br>style: """ + style + """, 
                 <br>type: """ + type + """, 
                 <br>age: """ + age + """, 
                 <br>religion: """ + religion + """, 
                 <br>free: """ + free + """, 
                 """
                messages.add_message(request, messages.INFO, mark_safe(string + ' for ' + request.session['child_id']))
            else:
                messages.add_message(request, messages.INFO, 'No child selected')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.INFO, 'No child selected')
        # messages.add_message(request, messages.INFO, str(i.id) + 'Added to ' + request.session['child_id'])


def export_selected_objects(self, request, queryset):
    selected = queryset.values_list('pk', flat=True)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect('/export/?ct=%s&ids=%s' % (
        ct.pk,
        ','.join(str(pk) for pk in selected),
    ))


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'Gender', 'Name', 'Phone', 'Last_Institute',
                    'Graduation_Institute', 'Graduation_Subject',
                    'HSC_Institute', 'HSC_Subject',
                    'HSC_GPA', 'Gender',
                    'Rating', 'RatedPerson']
    list_filter = ('PresentArea', 'Last_Institute', 'Graduation_Subject', 'Gender',
                   ('PreferredArea', custom_titled_filter('Preferred Area')),
                   'SSC_MEDIUM',
                   # Last medium
                   # Prefred subject
                   'SSC_Institute', 'SSC_Subject', 'SSC_GPA', 'SSC_GOLDEN', 'SSC_MEDIUM',
                   'HSC_Institute', 'HSC_Subject', 'HSC_GPA', 'HSC_GOLDEN',
                   'HSC_MEDIUM',
                   'Graduation_Institute',
                   'Graduation_Institute__Category',
                   'Graduation_Subject',
                   # 'PresentLocation',
                   'PermanentLocation',
                   # ('PreferredArea', custom_titled_filter('Preferred Area')),
                   # 'Location3',
                   'Religion', 'Age',
                   'BAN', 'Type',
                   'Rating', 'RatedPerson',
                   'Reminder',
                   ('Experience__Preferred_Medium', custom_titled_filter('Experienced Medium')),
                   ('Experience__Preferred_Education', custom_titled_filter('Experienced Class')),
                   ('Experience__Preferred_Subject', custom_titled_filter('Experienced Subject')),
                   ('Preferred__Preferred_Education', custom_titled_filter('Preferred Class ')),
                   ('Preferred__Preferred_Medium', custom_titled_filter('Preferred Medium')),
                   ('Preferred__Preferred_Subject', custom_titled_filter('Preferred Subject')),
                   'Abroad', 'IELTS', 'TOFEL', 'GMAT', 'GRE',
                   'Post_Graduation_Institute',
                   ('Graduation_Institute__Category', custom_titled_filter('Graduation Category')),
                   ('Post_Graduation_Institute__Category', custom_titled_filter('Post Graduation Category')),
                   'Post_Graduation_Subject',  'HSC_MEDIUM_Curriculum', 'SSC_MEDIUM_Curriculum',
                   'ImATeacherOf', 'TuitionStyle', 'Admission',  ('ImATeacherOf', custom_titled_filter('Institute Teacher')),
                   'CoachingCenterName',

                    'BloodGroup',  'PresentLocationThana', 'PermanentLocationThana',


                   'Physiotherapist',
                   'HandWriting', 'Hafiz', 'Music', 'Dance', 'Emergency', 'SSC_Year', 'Cadet',

                   )

    search_fields = [
        'Name', 'Email', 'Phone', 'Graduation_Institute__Name',
        'Graduation_Institute__SHORT', 'Graduation_Subject__Title',
        'Graduation_Subject__SHORT', 'Graduation_GPA',
        'HSC_Institute', 'HSC_Subject__Title',
        'HSC_Subject__SHORT', 'HSC_GPA',
        'SSC_Institute', 'SSC_Subject__Title',
        'SSC_Subject__SHORT', 'SSC_GPA',
        'HSC_GOLDEN', 'SSC_GOLDEN',
        'Expertise',
        'Experience__Preferred_Education', 'Experience__Preferred_Medium',
        'Experience__Preferred_Subject__Title',
        'Experience__Preferred_Subject__SHORT',
        'Experience__Other',
        'Important_Note', 'Note',
        'PresentLocation', 'PermanentLocation',
        'Location2', 'Location3',
        'Location4', 'Reminder', 'id', 'Religion', 'Age', 'PreferredArea__Name',
        'PresentArea__Name', 'Facebook_Link', 'Guardian_phone', 'ExpectedSalary', 'CoachingCenterName'
    ]
    actions_on_bottom = True,
    actions = [set_teacher, see_requirements]


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Division', ]
    search_fields = ['Name',]


class ThanaAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'District', ]
    list_filter = ['District']
    search_fields = ['Name',]


class ClassesSubjectAdmin(admin.ModelAdmin):
    list_display = ['Class', 'Medium', ]
    list_filter = ['Subject', 'Class', 'Medium', ]
    search_fields = ['Subject', 'Class', 'Medium', ]


admin.site.register(Areas)
admin.site.register(District, DistrictAdmin)
admin.site.register(Division)
admin.site.register(Thana, ThanaAdmin)
admin.site.register(ClassesSubject, ClassesSubjectAdmin)
