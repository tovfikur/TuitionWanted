import datetime
from django.db.models.signals import post_save
from django.db import models
from GuardianArea.models import Child, GuardianDetails
from Teacher.models import Teacher
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django_currentuser.middleware import get_current_user
from django.contrib.auth import login
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class Reminder(models.Model):
    User = models.ForeignKey('FollowUp.User', on_delete=models.DO_NOTHING, null=False, blank=False)
    Time = models.DateTimeField(null=False, blank=False)
    Note = models.JSONField(null=True, blank=True)
    # Note = models.TextField(null=True, blank=True)


# Teacher Reminder Receiver

def set_reminder(sender, instance, **kwargs):
    try:
        note = {"teacher": instance.id, "note": instance.ReminderNote}
        rdobj = Reminder.objects.create(User_id=int(get_current_user().id), Time=instance.Reminder, Note=note)
        rdobj.save()
    except:
        pass

# post_save.connect(set_reminder, sender=Teacher)


class User(AbstractUser):
    objects = UserManager()
    username = models.CharField(max_length=35, unique=True)
    email = models.EmailField('email address', blank=True, null=True)
    is_Checker = models.BooleanField(default=False)
    is_FollowUpper = models.BooleanField(default=False)
    is_Reserves = models.BooleanField(default=False)
    is_OfferCatcher = models.BooleanField(default=False)
    is_Guardian = models.BooleanField(default=False)
    is_Teacher = models.BooleanField(default=False)
    # personal info
    Phone_Number = PhoneNumberField(blank=False, null=False, default='+8801796693300')
    Avatar = models.ImageField(blank=True, null=True)
    Job_Title = models.CharField(max_length=20, null=True, blank=True)
    Job_Shift = models.TimeField(blank=True, null=True)
    NID = models.FileField(blank=True, null=True)
    Proof_Of_Presence = models.FileField(blank=True, null=True)
    Guardian = models.ManyToManyField(GuardianDetails, blank=True)
    Teacher = models.ManyToManyField(Teacher, blank=True)


class TemporaryTuitionForChild(models.Model):
    Child = models.OneToOneField(Child, on_delete=models.CASCADE, blank=False, null=False, default=1)
    Teacher = models.ManyToManyField(to=Teacher)
    Talks = models.CharField(max_length=200, null=True, blank=True)
    TalksJson = models.JSONField( null=True, blank=True)


class ShortListedTuitionForChild(models.Model):
    Child = models.OneToOneField(Child, on_delete=models.CASCADE, blank=False, null=False, default=1)
    Teacher = models.ManyToManyField(to=Teacher)
    Talks = models.CharField(max_length=200, null=True, blank=True)
    TalksJson = models.JSONField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     try:
    #         temporary_child_obj = TemporaryTuitionForChild.objects.filter(Child = self.Child)
    #         for i in temporary_child_obj:
    #             for temporary_teacher in i.Teacher.all():
    #                 for self_teacher in self.Teacher.all():
    #                     if temporary_teacher == self_teacher:
    #                         self.TalksJson = i.TalksJson
    #     except:
    #         pass
    #     super().save(*args, **kwargs)


class AssignedTeacherForChild(models.Model):
    Child = models.ForeignKey(Child, on_delete=models.CASCADE)
    Teacher = models.ManyToManyField(to=Teacher)
    Talks = models.CharField(max_length=200, null=True, blank=True)
    TalksJson = models.JSONField(null=True, blank=True)


class DemoTeacherForChild(models.Model):
    Child = models.ForeignKey(Child, on_delete=models.CASCADE)
    Teacher = models.ManyToManyField(to=Teacher)
    Talks = models.CharField(max_length=200, null=True, blank=True)
    TalksJson = models.JSONField(null=True, blank=True)
    permanent = models.BooleanField(default=False)


class PermanentTuitionForChild(models.Model):
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Child = models.ForeignKey(Child, on_delete=models.CASCADE)
    money = models.SmallIntegerField(null=True, blank=True)
    Reminder = models.DateTimeField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    TalksJson = models.JSONField(null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)

    def save(self, *args, **kwargs):
        try:
            self.Reminder = datetime.datetime.now()
        except:
            pass
        super().save(*args, **kwargs)


class GuardianHistory(models.Model):
    Guardian = models.ForeignKey(GuardianDetails, on_delete=models.CASCADE, blank=False, null=False, default=1)
    Child = models.ForeignKey(Child, on_delete=models.DO_NOTHING, blank=False, null=False)
    Teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, blank=False, null=False)
    Salary = models.IntegerField(blank=False, null=False, default=3000)
    Note = models.TextField(blank=True, null=True)
    OfferCatcher = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, null=True,
                                     related_name='OfferCatcher')
    Reserver = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, null=True,
                                 related_name='Reserver')
    FollowUpper = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, null=True,
                                    related_name='FollowUpper')
    Checker = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, null=True,
                                related_name='Checker')
    Time = models.DateTimeField(auto_now_add=True, )


class TeacherHistory(models.Model):
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=1)
    Child = models.ForeignKey(Child, on_delete=models.CASCADE, blank=False, null=False)
    Salary = models.IntegerField(blank=False, null=False, default=3000)
    Starting_Date = models.DateField(auto_now_add=True)
    Ending_Date = models.DateField(blank=True, null=True)
    Note = models.TextField(blank=True, null=True)


class EmployeeLoginHistory(models.Model):
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    Date = models.DateField(auto_now_add=True)
    Login = models.TimeField(blank=True, null=True)
    Logout = models.TimeField(blank=True, null=True)


class SMS(models.Model):
    sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    number = PhoneNumberField()
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.sender)


# signals

def teacher_post_created(sender, instance, created, *args, **kwargs):
    if created:
        user = User.objects.create_user(username=str(str(instance.Phone).replace('+88', '')), email=instance.Email, password=instance.Password)
        user.Phone_Number = instance.Phone
        user.is_Teacher = True
        user.save()
        ins_obj = Teacher.objects.get(id=instance.id)
        ins_obj.auth = user
        ins_obj.save()
post_save.connect(teacher_post_created, sender=Teacher)


def guardian_post_created(sender, instance, created, *args, **kwargs):
    if created:
        user = User.objects.create_user(username=str(str(instance.Phone).replace('+88', '')), email=instance.Email, password=instance.Password)
        user.Phone_Number = instance.Phone
        user.is_Guardian = True
        user.save()
        ins_obj = GuardianDetails.objects.get(id=instance.id)
        ins_obj.auth = user
        ins_obj.save()
post_save.connect(guardian_post_created, sender=GuardianDetails)

