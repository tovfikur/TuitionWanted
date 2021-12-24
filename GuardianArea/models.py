import re
from django.template.defaultfilters import slugify
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

import FollowUp.models
import GuardianArea.models
from Teacher.models import Teacher, University, Subject
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import get_current_user
from django.utils.http import int_to_base36
import datetime
import time
# Create your models here.


# Student Choices
LEVEL_CHOICE = ((1, 'Class 0'), (1, 'Class 1'),
                (2, 'Class 2'), (3, 'Class 3'),
                (4, 'Class 4'), (5, 'Class 5'),
                (6, 'Class 6'), (7, 'Class 7'),
                (8, 'Class 8'), (9, 'Class 9'),
                (10, 'Class 10'), (11, 'Class 11'),
                (12, 'Class 12'), (13, 'Diploma'),
                (14, 'Degree'), (15, 'Honors'),
                (16, 'O-Level'), (17, 'A-Level(AS)'),
                (19, 'pre-KG'), (18, 'KG'),
                (20, 'A-Level(A2)'), (21, 'SSC Examine'), (22, 'HSC Examine'), (23, 'Admission'),
                (20, 'Others'),)


MEDIUM_CHOICE = ((1, 'Bangla Medium'), (2, 'English Medium'),
                 (3, 'English Version'), (4, 'Madrasa Medium'),
                 (7, 'Education of Quran'),
                 (9, 'Any'),
                 (8, 'Others'),
                 )


GENDER_CHOICE = ((1, 'Male'), (2, 'Female'), (4, 'Any'), (3, 'Other'))
TYPE_CHOICE = ((1, 'Normal'), (2, 'Special'),)

# Teacher Choices

Teacher_GENDER_CHOICE = ((1, 'Male'), (2, 'Female'), (3, 'Other'), (4, 'Male/Female'))
Teacher_LEVEL_CHOICE = ((0, 'Secondary'), (1, 'Higher Secondary'), (3, 'Honors'), (5, 'Masters'), (4, 'Others'), (6, 'Any'))
Teacher_XP_CHOICE = ((0, 'No experience needed'), (1, '1/2 years experience'),
                     (2, '3/5 years experience'), (3, 'More than 5 years experience'))
Teacher_AGE_CHOICE = ((0, '<20'), (1, '21-25'), (2, '26-35'), (3, '>35'), (4, 'Any'))
Teacher_BACKGROUND_CHOICE = ( (1, 'General'), (2, 'Science'), (3, 'Engineer'),
                             (4, 'Medical'), (5, 'Arts'), (6, 'Commerce'),
                             (7, 'Technical'), (8, 'English Medium'), (9, 'English Version'), (10, 'Education of Quran'),
                              (11, 'Other'), (100, 'Any'),)
Free_DURATION_CHOICE = ((datetime.timedelta(hours=1), '01 Hour'),
                        (datetime.timedelta(hours=1.5), '01H 30M'),
                        (datetime.timedelta(hours=2), '02 Hour'),
                        (datetime.timedelta(hours=2.5), '02H 30M'),
                        (datetime.timedelta(hours=3), '03 Hour')
                        )
Teacher_Religion_CHOICE = ((0, 'Islam'), (1, 'Hinduism '), (2, 'Buddhism '), (3, 'Christianity'), (4, 'Others'), (5, 'Any'))
TUITION_STYLE = ((1, 'Home tuition'), (2, 'Group'), (3, 'Course'), (4, 'Online'))


class Note(models.Model):
    Writer = CurrentUserField()
    Note = models.TextField(blank=True, null=True)
    Created = models.DateTimeField(blank=False, null=True, auto_now_add=True)

    def __str__(self):
        return str(self.Note) +'|'+ str(self.Writer)


def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value

def nested_tuple_text(index, x):
    for i in x:
        if i[0] == index:
            return i[1]


class Child(models.Model):
    slug = models.SlugField(max_length=5, blank=False, null=False, primary_key=True, default=0,  help_text='Do not change it')
    Name = models.CharField(max_length=40, blank=False, null=False, default='')
    Phone = models.CharField(max_length=20, blank=True, null=True, default='+8801')
    Address = models.CharField(max_length=200, null=True, blank=True)
    Education_Level = models.SmallIntegerField(choices=LEVEL_CHOICE, default=6)
    Expect_to_read = models.CharField(max_length= 300, null=True, blank=True)
    Education_Institute = models.CharField(max_length=200, null=True, blank=True)
    Education_Medium = models.SmallIntegerField(choices=MEDIUM_CHOICE, default=1)
    Gender = models.SmallIntegerField(choices=GENDER_CHOICE, default=2)
    Type = models.SmallIntegerField(choices=TYPE_CHOICE, default=1)
    Paid = models.BooleanField(default=False)
    Canceled = models.BooleanField(default=False)
    Note = models.ManyToManyField(Note, blank=True)
    Free_Time = models.TextField(blank=True, null=True)
    Free_Duration = models.DurationField(blank=True, null=True, choices=Free_DURATION_CHOICE, default=datetime.timedelta(hours=1.5))
    Important_Note = models.TextField(blank=True, null=True)
    Created = models.DateTimeField(blank=False, null=True, auto_now_add=True)
    Reserved = models.BooleanField(default=False)
    Leads = models.BooleanField(default=False)

    # Requirement
    Expected_Salary = models.IntegerField(null=True, blank=True, help_text='0 for Negotiable')
    PerClass = models.BooleanField(default=False)
    PerCourse = models.BooleanField(default=False)
    Expected_Day = models.IntegerField(null=True, blank=True)
    Expected_Style = models.SmallIntegerField(choices=TUITION_STYLE, default=1)
    Expected_Subjects = models.ManyToManyField(Subject, blank=True)
    Teacher_HSC_GOLD = models.BooleanField(default=False)
    Expected_School = models.CharField(max_length=150, blank=True)
    Expected_College = models.CharField(max_length=150, blank=True)
    Teacher_Gender = models.SmallIntegerField(choices=Teacher_GENDER_CHOICE, default=4)
    Teacher_Level = models.SmallIntegerField(choices=Teacher_LEVEL_CHOICE, default=3)
    Teacher_Background = models.SmallIntegerField(choices=Teacher_BACKGROUND_CHOICE, default=100)
    Teacher_Medium = models.SmallIntegerField(choices=MEDIUM_CHOICE, default=1)
    Teacher_Type = models.SmallIntegerField(choices=TYPE_CHOICE, default=1)
    Teacher_Experience = models.SmallIntegerField(choices=Teacher_XP_CHOICE, default=0)
    Teacher_Age = models.SmallIntegerField(choices=Teacher_AGE_CHOICE, default=6)
    Teacher_University = models.ManyToManyField(University, blank=True)
    Teacher_Religion = models.IntegerField(blank=True, null=True, choices=Teacher_Religion_CHOICE, default=5)
    Guardian = models.ForeignKey('GuardianArea.GuardianDetails', on_delete=models.DO_NOTHING, null=True, blank=True)
    active = models.BooleanField(default=True)
    is_reserved = models.BooleanField(default=True)
    is_short = models.BooleanField(default=True)
    is_assign = models.BooleanField(default=True)
    is_demo = models.BooleanField(default=True)
    is_permanent = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.Canceled:
            self.active = False
        try:
            if FollowUp.models.TemporaryTuitionForChild.objects.get(Child=self):
                self.is_reserved = True
        except:
            self.is_reserved = False

        try:
            if FollowUp.models.ShortListedTuitionForChild.objects.get(Child=self):
                self.is_reserved = False
                self.is_short = True
        except:
            self.is_short = False

        try:
            if FollowUp.models.AssignedTeacherForChild.objects.get(Child=self):
                self.is_reserved = False
                self.is_short = False
                self.is_assign = True
        except:
            self.is_assign = False

        try:

            if FollowUp.models.DemoTeacherForChild.objects.get(Child=self):
                self.is_reserved = False
                self.is_short = False
                self.is_assign = False
                self.is_demo = True
        except:
            self.is_demo = False

        try:
            if FollowUp.models.PermanentTuitionForChild.objects.get(Child=self):
                self.is_reserved = False
                self.is_short = False
                self.is_assign = False
                self.is_demo = False
                self.is_permanent = True
        except:
            self.is_permanent = False




    def __str__(self):
        return self.Name + ' (' + str(self.slug) + ')'

    def save(self, *args, **kwargs):
        if self.Guardian:
            obj = GuardianArea.models.GuardianDetails.objects.get(id=self.Guardian.id)
            obj.Child.add(self)
            obj.save()
        obj = None
        if not self.slug:
            slug_str = "%s %s %s 0" % (
            datetime.date.today().strftime('%y')[-1], self.gender_short_text(), datetime.date.today().strftime('%b'))
            unique_slugify(self, slug_str, slug_separator='')

        if get_current_user().is_Guardian:
            obj = GuardianDetails.objects.get(auth=get_current_user())
            # print(obj)
            super().save(*args, **kwargs)
            try:
                obj.Child.add(self)
            except:
                obj.Child.set(self)
        else:
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Tuition'
        verbose_name_plural = 'Tuition`s'


    def medium_text(self):
        return nested_tuple_text(self.Education_Medium, MEDIUM_CHOICE)

    def gender_text(self):
        if self.Teacher_Gender == 1:
            return 'Male'
        elif self.Teacher_Gender == 2:
            return 'Female'
        elif self.Teacher_Gender == 3:
            return 'Other'
        else:
            return 'Male/Female'

    def gender_short_text(self):
        if self.Teacher_Gender == 1:
            return 'M'
        elif self.Teacher_Gender == 2:
            return 'F'
        elif self.Teacher_Gender == 3:
            return 'O'
        else:
            return 'A'

    def t_university_text(self):
        vs = ''
        for i in self.Teacher_University.all():
            vs = i.SHORT + ',' + vs
        return vs

    def teacher_medium_text(self):
        for i in MEDIUM_CHOICE:
            if i[0] is self.Education_Medium:
                return MEDIUM_CHOICE[self.Education_Medium-1][1]
        return ''

    def background_text(self):
        nested_tuple_text(self.Teacher_Background, Teacher_BACKGROUND_CHOICE)

    def experience_text(self):
        for i in Teacher_XP_CHOICE:
            if i[0] is self.Teacher_Experience:
                return Teacher_XP_CHOICE[self.Teacher_Experience][1]

    def address_text(self):
        try:
            obj = GuardianDetails.objects.get(Child=self)
            return obj.Address
        except:
            return ''

    def level_text(self):
        for i in LEVEL_CHOICE:
            if i[0] is self.Education_Level :
                return LEVEL_CHOICE[self.Education_Level][1]

    def teacher_level_text(self):
        for i in Teacher_LEVEL_CHOICE:
            if i[0] is self.Teacher_Level:
                return Teacher_LEVEL_CHOICE[self.Teacher_Level-1][1]

    def subject_text(self):
        txt = ''
        for i in self.Expected_Subjects.all():
            txt = txt + i.SHORT + ', '
        return txt

    def style_text(self):
        for i in TUITION_STYLE:
            if i[0] is self.Expected_Style:
                return TUITION_STYLE[self.Expected_Style-1][1]

    def teacher_type_text(self):
        for i in TYPE_CHOICE:
            if i[0] is self.Teacher_Type:
                return TYPE_CHOICE[self.Teacher_Type-1][1]

    def teacher_age_text(self):
        for i in Teacher_AGE_CHOICE:
            if i[0] is self.Teacher_Age:
                return Teacher_AGE_CHOICE[self.Teacher_Age-1][1]

    def teacher_religion_text(self):
        for i in Teacher_Religion_CHOICE:
            if i[0] is self.Teacher_Religion:
                return Teacher_Religion_CHOICE[self.Teacher_Religion][1]

    def teacher_university_text(self):
        uni_str = ''
        for i in self.Teacher_University.all():
            uni_str = uni_str + i.SHORT + ', '
        return uni_str


class ChildGroup(models.Model):
    Child = models.ManyToManyField(Child, blank=True, verbose_name='Tuition')

    def __str__(self):
        return str(self.id)


class GuardianDetails(models.Model):
    auth = models.ForeignKey('FollowUp.User', null=True, blank=True, on_delete=models.CASCADE, related_name='auth')
    Name = models.CharField(max_length=40, blank=False, null=True, default='Tovfikur Rahman')
    Phone = models.CharField(max_length=20, blank=False, null=False, default='+8801', unique=True)
    Email = models.EmailField(blank=True, null=True)
    Password = models.CharField(max_length=20, blank=False, null=False, default='+8801')
    Address = models.CharField(max_length=250, null=True, blank=True)
    LastAddress = models.CharField(max_length=250, null=True, blank=True)
    Profession = models.CharField(blank=True, null=True, max_length=100)
    Expected_Range = models.SmallIntegerField(blank=True, null=True)
    # Note = models.ManyToManyField(Note, blank=True)
    Important_Note = models.TextField(blank=True, null=True)
    Rating = models.SmallIntegerField(blank=True, null=True)
    Ban = models.BooleanField(default=False)
    Child = models.ManyToManyField(Child, blank=True, verbose_name='Tuition')
    Child_Group = models.ManyToManyField(ChildGroup, blank=True, verbose_name='Tuition Group')
    NID = models.ImageField(blank=True, null=True, upload_to='NID')
    Reminder = models.DateTimeField(blank=True, null=True)
    Created = models.DateTimeField(blank=False, null=True, auto_now_add=True)
    Connect = models.ForeignKey('FollowUp.User', on_delete=models.DO_NOTHING, blank=True, null=True)

    # Partner
    Partner_Phone = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return str(self.Name) + ' ( ' + str(self.id) + ' )' + ' ( ' + str(self.Phone) + ' )'

    def save(self, *args, **kwargs):
        try:
            user_obj = self.Connect
            user_obj.Guardian.add(self)
            user_obj.save()
        except:
            pass
        super().save(*args, **kwargs)


class Post(models.Model):
    Time = models.DateTimeField(blank=True, null=True)
    Text = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.Time)
