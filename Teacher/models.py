from phonenumber_field.modelfields import PhoneNumberField
import sys
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your models here.
import datetime

YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r, r))

TEACHING_LEVEL_CHOICE = (
    (0, 'Nursery/Play/KG'),
    (1, 'Class 1'),
    (2, 'Class 2'),
    (3, 'Class 3'),
    (4, 'Class 4'),
    (5, 'Class 5'),
    (6, 'Class 6'),
    (7, 'Class 7'),
    (8, 'Class 8'),
    (9, 'Class 9 / O Level'),
    (10, 'Class 10 / O Level'),
    (11, 'Class 11 / AS'),
    (12, 'Class 12 / A2'),
    (20, 'Others'),
)

Teacher_AGE_CHOICE = ((0, '<20'), (1, '21-25'), (2, '26-35'), (3, '>35'))
Teacher_Religion_CHOICE = ((0, 'Islam'), (1, 'Hinduism '), (2, 'Buddhism '), (3, 'Christianity'), (4, 'Others'))

TEACHING_MEDIUM_CHOICE = (
    (1, 'Bangla Medium'),
    (2, 'English Medium'),
    (3, 'English Version'),
    (4, 'Madrasha Medium'),
    (6, 'Technical'),
    (8, 'Others'),
)

GENDER_CHOICE = (
    (1, 'Male'),
    (2, 'Female'),
    (3, 'Other')
)

TYPE_CHOICE = (
    (1, 'Normal Child'),
    (2, 'Autistic/Special Child'),
)

BLOOD_CHOICE = (
    (1, 'A+'),
    (2, 'A-'),
    (3, 'B+'),
    (4, 'B-'),
    (5, 'O+'),
    (6, 'O-'),
    (7, 'AB+'),
    (8, 'AB-'),
)

TUITION_STYLE = ((1, 'Home tuition'), (2, 'Group'), (3, 'Course'), (4, 'Online'), (5, 'Group and Course'),
                 (7, 'Home Tuition and Online'), (7, 'Home Tuition and Group'), (6, 'All'),)

# UNIVERSITY_CATEGORY = ((1, 'Public'), (2, 'Private'), (3, 'National'), (4, 'Others'),)

def nested_tuple_text(index, x):
    for i in x:
        if i[0] == index:
            return i[1]


class Division(models.Model):
    Name = models.CharField(unique=True, max_length=150, null=False, blank=True, default='Dhaka')

    class Meta:
        ordering = ['Name']

    def __str__(self):
        return self.Name


class District(models.Model):
    Division = models.ForeignKey(Division, null=False, blank=False, on_delete=models.CASCADE, default=8)
    Name = models.CharField(max_length=150, null=True, blank=True, unique=True)

    class Meta:
        ordering = ['Name']

    def __str__(self):
        return self.Name+'  ' + str(self.id)


class Thana(models.Model):
    District = models.ForeignKey(District, null=False, blank=False, on_delete=models.CASCADE,  default=74)
    Name = models.CharField(max_length=150, null=True, blank=True, unique=True)

    class Meta:
        ordering = ['Name']

    def __str__(self):
        return self.Name+'  ' + str(self.id)


class University(models.Model):
    Name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    SHORT = models.CharField(max_length=10, null=True, blank=True)
    URL = models.URLField(null=True, blank=True)
    Category = models.SmallIntegerField(
                                choices=((1, 'PUBLIC'), (2, 'NATIONAL'), (3, 'PRIVATE'), (4, 'OTHERS'), ),
                                blank=True, null=True)

    def fullname(self):
        return str(self.Name) + ' | ' + str(self.SHORT)
               # ' | ' + self.Private

    def __str__(self):
        return str(self.Name)

    class Meta:
        ordering = ["Name"]


class Schools(models.Model):
    Name = models.CharField(max_length=100, null=True, blank=True)
    SHORT = models.CharField(max_length=10, null=True, blank=True)
    URL = models.URLField(null=True, blank=True)

    def fullname(self):
        return str(self.Name) + ' | ' + str(self.SHORT)
               # ' | ' + self.Private

    def __str__(self):
        return str(self.Name)

    class Meta:
        ordering = ["Name"]


class Subject(models.Model):
    Title = models.CharField(max_length=110, null=True, blank=True, unique=True)
    SHORT = models.CharField(max_length=10, null=True, blank=True)
    URL = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["Title"]

    def __str__(self):
        return self.Title


class ClassesSubject(models.Model):
    Class = models.IntegerField(choices=TEACHING_LEVEL_CHOICE, null=True, blank=True)
    Medium = models.IntegerField(choices=TEACHING_MEDIUM_CHOICE, null=True, blank=True)
    Subject = models.ManyToManyField(Subject, null=True, blank=True)

    def __str__(self):
        return nested_tuple_text(self.Class, TEACHING_LEVEL_CHOICE)


class TeachingSection(models.Model):
    Preferred_Education = models.SmallIntegerField(choices=TEACHING_LEVEL_CHOICE, default=20)
    Preferred_Medium = models.SmallIntegerField(choices=TEACHING_MEDIUM_CHOICE, default=1)  # filter
    Preferred_Subject = models.ManyToManyField(Subject, blank=True)  # filter
    Other = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        sub = ''
        for i in self.Preferred_Subject.all():
            sub =  str(i.Title) + ', '+str(sub)

        return str(self.id) + ' ' + str(nested_tuple_text(self.Preferred_Education, TEACHING_LEVEL_CHOICE)) + ' | ' +\
               str(nested_tuple_text(self.Preferred_Medium, TEACHING_MEDIUM_CHOICE)) + ' | ' + \
               sub

    def pre_med(self):
        return nested_tuple_text(self.Preferred_Medium, TEACHING_MEDIUM_CHOICE)

    def pre_edu(self):
        return nested_tuple_text(self.Preferred_Education, TEACHING_LEVEL_CHOICE)


class Areas(models.Model):
    Name = models.CharField(max_length=200, default='Dhaka')

    def __str__(self):
        return self.Name


class SSC_HSC_Group(models.Model):
    Title = models.CharField(max_length=200, default='Science')
    SHORT = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.Title



class Teacher(models.Model):
    auth = models.ForeignKey('FollowUp.User', null=True, blank=True, on_delete=models.CASCADE)
    Name = models.CharField(max_length=40, default="", null=False, blank=False)  # contain search
    Email = models.EmailField(null=True, blank=True)  # ext search
    Phone = models.CharField(blank=True, max_length=300, null=True, unique=True)  # ext search
    Password = models.CharField(max_length=32, null=True, blank=True)
    Facebook_Link = models.URLField(blank=True, null=True)
    Guardian_phone = models.CharField(blank=True, max_length=300, null=True)
    Refer_phone = models.CharField(blank=True, max_length=300, null=True)
    Refer_Name = models.CharField(max_length=40, default="", null=True, blank=True) # contain search
    Avatar = models.ImageField(blank=True, null=True, upload_to='Avatar')
    BloodGroup = models.IntegerField(choices=BLOOD_CHOICE, null=True, blank=True)
    Age = models.IntegerField(blank=True, null=True, choices=Teacher_AGE_CHOICE)
    BirthDate = models.DateField(blank=True, null=True)
    Religion = models.IntegerField(blank=True, null=True, choices=Teacher_Religion_CHOICE)
    Gender = models.SmallIntegerField(choices=GENDER_CHOICE, default=1, null=True, blank=True)  # filter
    Type = models.SmallIntegerField(choices=TYPE_CHOICE, default=1, null=True, blank=True)

    Post_Graduation_Institute = models.ForeignKey(University, blank=True, null=True, on_delete=models.DO_NOTHING,
                                              related_name='PG_Institute')  # filter
    Post_Graduation_Subject = models.ForeignKey(Subject, blank=True, null=True, on_delete=models.DO_NOTHING,
                                            related_name='PG_Subject')  # filter
    Post_Graduation_GPA = models.FloatField(blank=True, null=True)  # filter
    Post_Graduation_Year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)  # sort

    Graduation_Institute = models.ForeignKey(University, blank=True, null=True, on_delete=models.DO_NOTHING)  # filter
    Oth_Graduation_Institute = models.CharField(max_length=300, blank=True, null=True)  # search
    Graduation_Subject = models.ForeignKey(Subject, blank=True, null=True, on_delete=models.DO_NOTHING)  # filter
    Graduation_GPA = models.FloatField(blank=True, null=True)  # filter
    Graduation_Year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)  # sort

    HSC_Institute = models.CharField(max_length=150, blank=True, null=True)  # filter
    HSC_Subject = models.ForeignKey(SSC_HSC_Group, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='HSC_SUB')  # filter
    HSC_GPA = models.FloatField(blank=True, null=True)  # filter
    HSC_MEDIUM = models.IntegerField(choices=TEACHING_MEDIUM_CHOICE, blank=True, null=True)  # filter
    HSC_MEDIUM_Curriculum = models.IntegerField(choices=((1, 'Edexcel'), (2, 'Cambridge'), (3, 'IB'), (4, 'Others')), blank=True, null=True)  # filter
    HSC_GOLDEN = models.BooleanField(null=True, blank=True, default=False)
    HSC_Year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)  # sort
    Cadet = models.BooleanField(default=False)

    SSC_Institute = models.CharField(max_length=150, blank=True, null=True)  # filter
    SSC_Subject = models.ForeignKey(SSC_HSC_Group, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='SSC_SUB')  # filter
    SSC_MEDIUM = models.IntegerField(choices=TEACHING_MEDIUM_CHOICE, blank=True, null=True)  # filter
    SSC_MEDIUM_Curriculum = models.IntegerField(choices=((1, 'Edexcel'), (2, 'Cambridge'), (3, 'IB'), (4, 'Others')), blank=True, null=True)  # filter
    SSC_GPA = models.FloatField(blank=True, null=True)  # filter
    SSC_GOLDEN = models.BooleanField(null=True, blank=True, default=False)
    SSC_Year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)  # sort

    TuitionStyle = models.SmallIntegerField(choices=TUITION_STYLE, null=True, blank=True, default=2500)
    ExpectedSalary = models.IntegerField(null=True, blank=True, default=2500)
    Experience = models.ManyToManyField(TeachingSection, blank=True, related_name='Experience')
    Preferred = models.ManyToManyField(TeachingSection, blank=True,  related_name='Preferred')
    Expertise = models.CharField(max_length=150, blank=True, )  # filter
    Running_Tuition = models.IntegerField(default=0, null=True, blank=True)  # sort

    PresentArea = models.ForeignKey(Areas, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='PresentArea', help_text='Select our zone')

    PresentLocation = models.CharField(max_length=100, blank=True, null=True, help_text='Full Address with house number')  # filter
    PresentLocationDivision = models.ForeignKey(Division, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='PresentLocationDivision')  # filter
    PresentLocationDistrict = models.ForeignKey(District, max_length=100, blank=True, null=True,  on_delete=models.DO_NOTHING, related_name='PresentLocationDistrict')  # filter
    PresentLocationThana = models.ForeignKey(Thana, max_length=100, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='PresentLocationThana')  # filter

    PermanentLocation = models.CharField(max_length=100, blank=True, null=True)  # filter
    PermanentLocationDivision = models.ForeignKey(Division, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='PermanentLocationDivision')  # filter
    PermanentLocationDistrict = models.ForeignKey(District, max_length=100, blank=True, null=True,  on_delete=models.DO_NOTHING, related_name='PermanentLocationDistrict')  # filter
    PermanentLocationThana = models.ForeignKey(Thana, max_length=100, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='PermanentLocationThana')  # filter

    PreferredArea = models.ManyToManyField(Thana, blank=True, null=True, related_name='PreferredArea')
    Location2 = models.CharField(max_length=100, blank=True, null=True)  # filter
    Location3 = models.CharField(max_length=100, blank=True, null=True)  # filter
    Location4 = models.CharField(max_length=100, blank=True, null=True)  # filter

    Last_Institute = models.CharField(max_length=150, blank=True, null=True)
    Last_Medium = models.CharField(max_length=50, blank=True, null=True)

#Extented
    Abroad = models.BooleanField(default=False)
    AbroadUniversity = models.CharField(max_length=200, null=True, blank=True)
    IELTS = models.BooleanField(default=False)
    IELTSPoint = models.CharField(null=True, blank=True, max_length=200)
    TOFEL = models.BooleanField(default=False)
    TOFELPoint = models.CharField(null=True, blank=True, max_length=200)
    GMAT = models.BooleanField(default=False)
    GMATPoint = models.CharField(null=True, blank=True, max_length=200)
    GRE = models.BooleanField(default=False)
    GREPoint = models.CharField(null=True, blank=True, max_length=200)
    Physiotherapist = models.BooleanField(default=False)
    ImATeacherOf = models.SmallIntegerField(choices=((1, 'School'),
                                                       (2, 'College'),
                                                       (5, 'Madrasa'),
                                                       (3, 'University'), (4, 'Coaching')),
                                              blank=True, null=True)
    CoachingCenterName = models.CharField(max_length=200, null=True, blank=True,
                                          help_text='Fill if you are a coaching teacher')

    HandWriting = models.SmallIntegerField(choices=((1, 'Average'), (2, 'Good'), (3, 'Expert')), default=1, null=True,
                                           blank=True)
    Music = models.BooleanField(default=False)
    Dance = models.BooleanField(default=False)
    MartialArts = models.BooleanField(default=False)
    Drawing = models.BooleanField(default=False)
    Hafiz = models.BooleanField(default=False)
    Spoken = models.BooleanField(default=False)
    Admission = models.SmallIntegerField(choices=((1, 'Engineering'), (2, 'Medical'), (3, 'University'), (4, 'Cadet')),
                                         null=True, blank=True)

    Note = models.TextField(blank=True, null=True)
    Important_Note = models.TextField(blank=True, null=True)
    Rating = models.FloatField(blank=True, null=True, default=0, )  # sort
    RatedPerson = models.IntegerField(blank=True, null=True, default=0)  # sort
    BAN = models.BooleanField(default=False, null=True, blank=True)  # filter
    Certificate = models.ImageField(blank=True, null=True, upload_to='Certificate')
    NID = models.ImageField(blank=True, null=True, upload_to='NID')
    StudentID = models.ImageField(blank=True, null=True, upload_to='SID')
    ReminderNote = models.CharField(max_length=200, blank=True, null=True)  # sort
    Reminder = models.DateTimeField(blank=True, null=True)  # sort
    Emergency = models.BooleanField(blank=True, null=True)

    def get_avatar(self):
        try:
            return self.Avatar.url
        except Exception:
            return 'https://www.pinclipart.com/picdir/middle/499-4992513_avatar-avatar-png-clipart.png'

    def get_nid(self):
        try:
            return self.NID.url
        except Exception:
            return '/static/vendor/adminlte/img/user2-160x160.jpg'

    def get_crt(self):
        try:
            return self.Certificate.url
        except Exception:
            return '/static/vendor/adminlte/img/user2-160x160.jpg'

    def religion_text(self):
        return nested_tuple_text(self.Religion, Teacher_Religion_CHOICE)

    def gender_text(self):
        return nested_tuple_text(self.Gender, GENDER_CHOICE)

    def __init__(self, *args, **kwargs):
        super(Teacher, self).__init__(*args, **kwargs)
        self.initial_Rating = self.Rating
        self.initial_RatedPerson = self.RatedPerson
        self.initial_ReminderNote = self.ReminderNote
        self.initial_Reminder = self.Reminder
        self.initial_Avatar = self.Avatar
        self.initial_NID = self.NID
        self.initial_StudentID = self.StudentID
        self.initial_Certificate = self.Certificate
        self.initial_Oth_Graduation_Institute = self.Oth_Graduation_Institute

    def __str__(self):
        return self.Name + ' (' + str(self.id) + ')'

    def save(self, *args, **kwargs):

        # try:
        #     uni_obj = University.objects.create(Name=self.Oth_Graduation_Institute, Category=2)
        #     uni_obj.save()
        #     self.Graduation_Institute_id = uni_obj.id
        # except Exception as e:
        #     if 'UNIQUE constraint failed' in str(e):
        #         uni_obj = University.objects.get(Name=self.Oth_Graduation_Institute)
        #         self.Graduation_Institute_id = uni_obj.id
        #     pass

        try:
            if self.initial_Avatar:
                if not self.Avatar:
                    self.Avatar = self.initial_Avatar
        except:
            pass

        try:
            if self.initial_NID :
                if not self.NID:
                    self.NID = self.initial_NID
        except:
            pass

        try:
            if self.initial_StudentID:
                if not self.StudentID:
                    self.StudentID = self.initial_StudentID
        except:
            pass

        try:
            if self.initial_Certificate:
                if not self.Certificate:
                    self.Certificate = self.initial_Certificate
        except:
            pass

        try:
            self.auth.set_password(self.Password)
        except Exception as e:
            print(e)
            pass

        try:
            if not self.initial_Rating == self.Rating:
                if not self.initial_RatedPerson == self.initial_RatedPerson:
                    self.Rating = ((self.initial_Rating * self.initial_RatedPerson) +
                                  self.Rating)/(self.initial_RatedPerson + 1)
        except Exception as e:
            print(e)

        try:
            self.Last_Medium = nested_tuple_text(self.SSC_MEDIUM, TEACHING_MEDIUM_CHOICE)
        except:
            pass
        try:
            if not self.id:
                self.Avatar = self.compressImage(self.Avatar)
        except:
            pass
        try:
            if not self.id:
                self.NID = self.compressImage(self.NID)
        except:
            pass

        try:
            if not self.id:
                self.Certificate = self.compressImage(self.Certificate)
        except:
            pass
        if self.Post_Graduation_Institute:
            self.Last_Institute = self.Post_Graduation_Institute.fullname()
        elif self.Graduation_Institute:
            self.Last_Institute = self.Graduation_Institute.fullname()
        elif self.HSC_Institute:
            self.Last_Institute = self.HSC_Institute
        elif self.SSC_Institute:
            self.Last_Institute = self.Last_Institute
        else:
            pass

        if not (self.HSC_GPA == 5):
            self.HSC_GOLDEN = False
        if not (self.SSC_GPA == 5):
            self.SSC_GOLDEN = False
        if not (self.initial_Rating == self.Rating):
            try:
                self.Rating = round((self.initial_Rating + self.Rating) / self.initial_RatedPerson, 2)
                self.RatedPerson = self.RatedPerson + 1
            except:
                pass
        return super().save(*args, **kwargs)

    def compressImage(self, uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1020, 573))
        imageTemproary.save(outputIoStream, format='JPEG', quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage
