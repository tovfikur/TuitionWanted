import datetime

from django.views.generic import TemplateView
from django.db.models import Q
from django.db import IntegrityError
from django.forms.models import model_to_dict
# import json

from django_currentuser.middleware import get_current_user
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, \
    RetrieveUpdateAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.response import Response
from GuardianArea.models import GuardianDetails, ChildGroup, Child
from Teacher.models import Teacher
from .models import GuardianHistory, TeacherHistory, Reminder
from .models import PermanentTuitionForChild, TemporaryTuitionForChild, \
    ShortListedTuitionForChild, AssignedTeacherForChild, DemoTeacherForChild, RoughNote
# Serializer
from .serializers import (GuardianListSerializer,
                          GuardianHistoryListSerializer,
                          TeacherDetailsSerializer,
                          TeacherHistorySerializer,
                          ChildGroupSerializer,
                          TemporaryTuitionForChildSerializer, ShortlistTuitionForChildSerializer,
                          ShortlistTuitionForChildCreateSerializer, PermanentTuitionForChildSerializer,
                          ChildSerializer, GuardianUpdateSerializer, ReminderSerializer, ChildSerializerRetrive)


# Create your views here.


class TestView(APIView):

    def get(self, request):
        return Response({'get': 'post'})


class ReminderListView(ListCreateAPIView):
    serializer_class = ReminderSerializer

    def get_queryset(self):
        return Reminder.objects.filter(User=self.request.user)


class ReminderListUpdateView(RetrieveUpdateAPIView):
    serializer_class = ReminderSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Reminder.objects.filter(User=self.request.user)


# Guardian section

class GuardianListView(ListAPIView):
    serializer_class = GuardianListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return self.request.user.Guardian


class GuardianDetailsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = GuardianDetails.objects.all()
    lookup_field = 'pk'
    serializer_class = GuardianListSerializer


class GuardianUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = GuardianDetails.objects.all()
    lookup_field = 'pk'
    serializer_class = GuardianUpdateSerializer


class ChildGroupView(RetrieveAPIView):
    queryset = ChildGroup.objects.all()
    serializer_class = ChildGroupSerializer


class GuardianHistoryView(ListAPIView):
    # queryset = GuardianHistory.objects.all()
    lookup_field = 'pk'
    serializer_class = GuardianHistoryListSerializer

    def get_queryset(self):
        return GuardianHistory.objects.filter(Guardian_id=self.kwargs['pk'])


class AddNoteToGuardian(APIView):
    def get(self, request, pk):
        obj = GuardianDetails.objects.get(pk=pk)
        obj.Note.add(request.GET.get('note'))
        obj.save()
        return Response(model_to_dict(obj.Note.get(id=obj.id)))


class AddNoteToChild(APIView):
    def get(self, request, pk):
        obj = Child.objects.get(slug=pk)
        obj.Note.add(request.GET.get('note'))
        obj.save()
        return Response(model_to_dict(obj.Note.get(id=obj.pk)))


class TemporaryTuitionForChildListView(ListAPIView):
    # queryset = TemporaryTuitionForChild.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TemporaryTuitionForChildSerializer
    pagination_class = None

    def get_queryset(self):
        try:
            return TemporaryTuitionForChild.objects.filter(Child__slug=self.request.GET['child'])
        except:
            return None


class ShortListCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = ShortlistTuitionForChildCreateSerializer
    queryset = ShortListedTuitionForChild.objects.all()


class ShortListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = ShortlistTuitionForChildSerializer

    # queryset = ShortListedTuitionForChild.objects.all()

    def get_queryset(self):
        try:
            return ShortListedTuitionForChild.objects.filter(Child__slug=self.request.GET['child'])
        except:
            return None


class AssignedShortListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = ShortlistTuitionForChildSerializer

    # queryset = ShortListedTuitionForChild.objects.all()

    def get_queryset(self):
        try:
            return AssignedTeacherForChild.objects.filter(Child__slug=self.request.GET['child'])
        except:
            return None


class DemoShortListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = ShortlistTuitionForChildSerializer

    # queryset = ShortListedTuitionForChild.objects.all()

    def get_queryset(self):
        try:
            return DemoTeacherForChild.objects.filter(Child__slug=self.request.GET['child'])
        except:
            return None


class PermanentCreateView(CreateAPIView):
    serializer_class = PermanentTuitionForChildSerializer
    queryset = PermanentTuitionForChild.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = None


class PermanentListView(ListAPIView):
    serializer_class = PermanentTuitionForChildSerializer
    queryset = PermanentTuitionForChild.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        try:
            return PermanentTuitionForChild.objects.filter(Child__slug=self.request.GET['child'])
        except:
            return None


def change_(obj, request, model, money=0):
    try:
        if obj.request.GET.get('cid'):
            if obj.request.GET.get('tid'):
                try:
                    obj = model.objects.get(Child_id=obj.request.GET.get('cid'))
                    obj.Teacher.add(obj.request.GET.get('tid'))
                    print(obj)
                except Exception as e:
                    if 'matching query does not exist' in str(e):
                        obj = model.objects.create(Child_id=obj.request.GET.get('cid'))
                        obj.Teacher.add(obj.request.GET.get('tid'))
                        print(obj)
        return 1
    except Exception as e:
        print(e)
        return 0


# Auto to Temporary


class AutoToTemporary(APIView):

    def get(self, request):
        try:
            if self.request.GET.get('cid'):
                if self.request.GET.get('tid'):
                    obj = TemporaryTuitionForChild.objects.create(Child_id=request.GET.get('cid'))
                    obj.Teacher.add(request.GET.get('tid'))
                    obj.save()
                    print(model_to_dict(obj))
            return Response({'ok': 1})
        except IntegrityError:
            obj = TemporaryTuitionForChild.objects.get(Child_id=request.GET.get('cid'))
            obj.Teacher.add(request.GET.get('tid'))
            obj.save()
            return Response({'ok': 1})
        except Exception as e:
            print(e)
            return Response({'error': str(e)})


# Temporary to Shortlisted
class TemporaryToShortList(APIView):
    def get(self, request):
        try:
            if self.request.GET.get('cid'):
                if self.request.GET.get('tid'):
                    try:
                        obj = ShortListedTuitionForChild.objects.get(Child_id=self.request.GET.get('cid'))
                        obj.Teacher.add(self.request.GET.get('tid'))
                        tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                        try:
                            note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                user=get_current_user(),
                                                                Text=str(tea_name.Name) + ' : ' + self.request.GET.get(
                                                                    'talk'))
                            note_obj.save()
                            tea_name.roughnotes.add(note_obj)
                            tea_name.save()
                            obj.TalksJson[self.request.GET.get('tid')] = str(
                                obj.TalksJson[self.request.GET.get('tid')]) + ' ' + self.request.GET.get('talk')
                            obj.save()
                        except Exception as e:
                            if '\'NoneType\' object does not support item assignment' in str(e):
                                note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                    user=get_current_user(),
                                                                    Text=str(tea_name) + ' : ' + self.request.GET.get(
                                                                        'talk'))
                                tea_name.roughnotes.add(note_obj)
                                tea_name.save()
                                note_obj.save()
                                obj.TalksJson = {self.request.GET.get('tid'): self.request.GET.get('talk')}
                                obj.save()
                    except Exception as e:
                        if 'matching query does not exist' in str(e):
                            obj = ShortListedTuitionForChild.objects.create(Child_id=self.request.GET.get('cid'))
                            try:
                                note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                    user=get_current_user(),
                                                                    Text=self.request.GET.get('talk'))
                                note_obj.save()
                                obj.TalksJson[self.request.GET.get('tid')] = str(
                                    obj.TalksJson[self.request.GET.get('tid')]) + ' ' + self.request.GET.get('talk')
                                obj.save()
                            except Exception as e:
                                if '\'NoneType\' object does not support item assignment' in str(e):
                                    tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                                    note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                        user=get_current_user(),
                                                                        Text=str(
                                                                            tea_name.Name) + ' : ' + self.request.GET.get(
                                                                            'talk'))
                                    tea_name.roughnotes.add(note_obj)
                                    tea_name.save()
                                    note_obj.save()
                                    obj.TalksJson = {self.request.GET.get('tid'): self.request.GET.get('talk')}
                                    obj.save()
                            obj.Teacher.add(self.request.GET.get('tid'))
            return Response({'ok': 1})
        except Exception as e:
            print(e)
            return Response({'error': str(e)})


# Temporary to Shortlisted
class ShortListToAssigned(APIView):
    def get(self, request):
        try:
            if self.request.GET.get('cid'):
                if self.request.GET.get('tid'):
                    try:
                        obj = AssignedTeacherForChild.objects.get(Child_id=self.request.GET.get('cid'))
                        obj.Teacher.add(self.request.GET.get('tid'))
                        try:
                            tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                            note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                user=get_current_user(),
                                                                Text=str(tea_name.Name) + ' : ' + self.request.GET.get(
                                                                    'talk'))
                            note_obj.save()
                            tea_name.roughnotes.add(note_obj)
                            tea_name.save()
                            obj.TalksJson[self.request.GET.get('tid')] = [str(
                                obj.TalksJson[self.request.GET.get('tid')]) + ' ' + self.request.GET.get('talk'),
                                                                          str(datetime.date.today())]
                            obj.save()
                        except Exception as e:
                            if '\'NoneType\' object does not support item assignment' in str(e):
                                tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                                note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                    user=get_current_user(),
                                                                    Text=str(
                                                                        tea_name.Name) + ' : ' + self.request.GET.get(
                                                                        'talk'))
                                tea_name.roughnotes.add(note_obj)
                                tea_name.save()
                                note_obj.save()
                                obj.TalksJson = {self.request.GET.get('tid'): self.request.GET.get('talk')}
                                obj.save()
                    except Exception as e:
                        if 'matching query does not exist' in str(e):
                            obj = AssignedTeacherForChild.objects.create(Child_id=self.request.GET.get('cid'))
                            try:
                                tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                                note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                    user=get_current_user(),
                                                                    Text=str(
                                                                        tea_name.Name) + ' : ' + self.request.GET.get(
                                                                        'talk'))
                                tea_name.roughnotes.add(note_obj)
                                tea_name.save()
                                note_obj.save()
                                obj.TalksJson[self.request.GET.get('tid')] = [str(
                                    obj.TalksJson[self.request.GET.get('tid')]) + ' ' + self.request.GET.get('talk'),
                                                                              str(datetime.date.today())]
                                obj.save()
                            except Exception as e:
                                if '\'NoneType\' object does not support item assignment' in str(e):
                                    tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                                    note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                        user=get_current_user(),
                                                                        Text=str(
                                                                            tea_name.Name) + ' : ' + self.request.GET.get(
                                                                            'talk'))
                                    tea_name.roughnotes.add(note_obj)
                                    tea_name.save()
                                    note_obj.save()
                                    obj.TalksJson = {self.request.GET.get('tid'): self.request.GET.get('talk')}
                                    obj.save()
                            obj.Teacher.add(self.request.GET.get('tid'))
                            print(obj)
            return Response({'ok': 1})
        except Exception as e:
            print(e)
            return Response({'error': str(e)})


# Short to Permanent

class AssignedToDemo(APIView):
    def get(self, request):
        try:

            if self.request.GET.get('cid'):
                if self.request.GET.get('tid'):
                    try:
                        obj = DemoTeacherForChild.objects.get(Child_id=self.request.GET.get('cid'))
                        obj.Teacher_id = self.request.GET.get('tid')
                        obj.money = self.request.GET.get('mny')
                        obj.User = self.request.user
                        try:
                            obj = DemoTeacherForChild.objects.create(Child_id=self.request.GET.get('cid'))
                            obj.Teacher.add(self.request.GET.get('tid'))
                            tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                            note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                user=get_current_user(),
                                                                Text=str(tea_name.Name) + ' : ' + self.request.GET.get(
                                                                    'talk'))
                            note_obj.save()
                            tea_name.roughnotes.add(note_obj)
                            tea_name.save()
                            obj.TalksJson[self.request.GET.get('tid')] = [str(
                                obj.TalksJson[self.request.GET.get('tid')]) + ' ' + self.request.GET.get('talk'),
                                                                          str(datetime.date.today())]
                            obj.save()
                        except Exception as e:
                            if '\'NoneType\' object does not support item assignment' in str(e):
                                tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                                note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                    user=get_current_user(),
                                                                    Text=str(
                                                                        tea_name.Name) + ' : ' + self.request.GET.get(
                                                                        'talk'))
                                tea_name.roughnotes.add(note_obj)
                                tea_name.save()
                                note_obj.save()
                                obj.TalksJson = {self.request.GET.get('tid'): self.request.GET.get('talk')}
                                obj.save()
                        obj.save()
                        print(obj)
                    except Exception as e:
                        if 'matching query does not exist' in str(e):
                            obj = DemoTeacherForChild.objects.create(Child_id=self.request.GET.get('cid'))
                            obj.Teacher.add(self.request.GET.get('tid'))
                            tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                            try:
                                note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                    user=get_current_user(),
                                                                    Text=str(
                                                                        tea_name.Name) + ' : ' + self.request.GET.get(
                                                                        'talk'))
                                tea_name.roughnotes.add(note_obj)
                                tea_name.save()
                                note_obj.save()
                                obj.TalksJson[self.request.GET.get('tid')] = [str(
                                    obj.TalksJson[self.request.GET.get('tid')]) + ' ' + self.request.GET.get('talk'),
                                                                              str(datetime.date.today())]
                                obj.save()
                            except Exception as e:
                                if '\'NoneType\' object does not support item assignment' in str(e):
                                    tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                                    note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                        user=get_current_user(),
                                                                        Text=str(
                                                                            tea_name.Name) + ' : ' + self.request.GET.get(
                                                                            'talk'))
                                    tea_name.roughnotes.add(note_obj)
                                    tea_name.save()
                                    note_obj.save()
                                    obj.TalksJson = {self.request.GET.get('tid'): self.request.GET.get('talk')}
                                    obj.save()
                            obj.money = self.request.GET.get('mny')
                            obj.User = self.request.user
                            obj.save()
                            print(obj)
                else:
                    obj = DemoTeacherForChild.objects.get(Child_id=self.request.GET.get('cid'))
                    obj.money = self.request.GET.get('mny')
                    obj.User = self.request.user
                    obj.save()
                    print(obj)
            return Response({'ok': 1})
        except Exception as e:
            print(e)
            return Response({'error': str(e)})


# Demo to permanent
class DemoToPermanent(APIView):
    def get(self, request):
        try:
            if self.request.GET.get('cid'):
                if self.request.GET.get('tid'):
                    try:

                        obj = PermanentTuitionForChild.objects.get(Child_id=self.request.GET.get('cid'))
                        obj.Teacher_id = self.request.GET.get('tid')
                        obj.money = self.request.GET.get('mny')
                        obj.User = self.request.user
                        tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                        try:
                            note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                user=get_current_user(),
                                                                Text=str(tea_name.Name) + ' : ' + self.request.GET.get(
                                                                    'talk'))
                            note_obj.save()
                            tea_name.roughnotes.add(note_obj)
                            tea_name.save()
                            obj.TalksJson[self.request.GET.get('tid')] = [str(
                                obj.TalksJson[self.request.GET.get('tid')]) + ' ' + self.request.GET.get('talk'),
                                                                          str(datetime.date.today())]
                            obj.save()
                        except Exception as e:
                            if '\'NoneType\' object does not support item assignment' in str(e):
                                tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                                note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                    user=get_current_user(),
                                                                    Text=str(
                                                                        tea_name.Name) + ' : ' + self.request.GET.get(
                                                                        'talk'))
                                tea_name.roughnotes.add(note_obj)
                                tea_name.save()
                                note_obj.save()
                                obj.TalksJson = {self.request.GET.get('tid'): self.request.GET.get('talk')}
                                obj.save()
                        obj.save()
                        temp_obj = DemoTeacherForChild.objects.get(Child__slug=self.request.GET.get('cid'))
                        temp_obj.permanent = True
                        temp_obj.save()
                    except Exception as e:
                        if 'matching query does not exist' in str(e):
                            obj = PermanentTuitionForChild.objects.create(Child_id=self.request.GET.get('cid'),
                                                                          Teacher_id=self.request.GET.get('tid'))
                            tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                            try:
                                note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                    user=get_current_user(),
                                                                    Text=str(
                                                                        tea_name.Name) + ' : ' + self.request.GET.get(
                                                                        'talk'))
                                tea_name.roughnotes.add(note_obj)
                                tea_name.save()
                                note_obj.save()
                                obj.TalksJson[self.request.GET.get('tid')] = [str(
                                    obj.TalksJson[self.request.GET.get('tid')]) + ' ' + self.request.GET.get('talk'),
                                                                              str(datetime.date.today())]
                                obj.save()
                            except Exception as e:
                                if '\'NoneType\' object does not support item assignment' in str(e):
                                    tea_name = Teacher.objects.get(id=self.request.GET.get('tid'))
                                    note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                                        user=get_current_user(),
                                                                        Text=str(
                                                                            tea_name.Name) + ' : ' + self.request.GET.get(
                                                                            'talk'))
                                    tea_name.roughnotes.add(note_obj)
                                    tea_name.save()
                                    note_obj.save()
                                    obj.TalksJson = {self.request.GET.get('tid'): self.request.GET.get('talk')}
                                    obj.save()
                            obj.money = self.request.GET.get('mny')
                            obj.User = self.request.user
                            obj.save()
                            temp_obj = DemoTeacherForChild.objects.get(Child__slug=self.request.GET.get('cid'))
                            temp_obj.permanent = True
                            temp_obj.save()
                else:
                    obj = PermanentTuitionForChild.objects.get(Child_id=self.request.GET.get('cid'))
                    obj.money = self.request.GET.get('mny')
                    obj.User = self.request.user
                    obj.save()
                    print(obj)
            return Response({'ok': 1})
        except Exception as e:
            print(e)
            return Response({'error': str(e)})


# Permanent to confirm

class AutoRecommendationView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = TeacherDetailsSerializer

    # queryset = Teacher.objects.all()
    def get_queryset(self):
        try:
            if self.request.GET.get('q'):
                t_obj = Teacher.objects.all()
                # t_obj = Teacher.objects.filter(Running_Tuition=)
                print(self.request.GET.get('name'))
                if self.request.GET.get('name'):
                    t_obj = t_obj.filter(Q(Name__icontains=self.request.GET.get('name')))

                if self.request.GET.get('email'):
                    t_obj = t_obj.filter(Q(Email=self.request.GET.get('email')))

                if self.request.GET.get('phone'):
                    t_obj = t_obj.filter(Q(Email=self.request.GET.get('phone')))

                if self.request.GET.get('exp'):
                    t_obj = t_obj.filter(Q(Expertise__icontains=self.request.GET.get('exp')))

                if self.request.GET.get('note'):
                    t_obj = t_obj.filter(Q(Expertise__icontains=self.request.GET.get('note')) |
                                         Q(Important_Note__icontains=self.request.GET.get('note')))

                if self.request.GET.get('institute'):
                    for i in self.request.GET.get('institute').split(','):
                        t_obj = t_obj.filter(Q(Graduation_Institute=i))

                if self.request.GET.get('subject'):
                    for i in self.request.GET.get('subject').split(','):
                        t_obj = t_obj.filter(Q(Graduation_Subject=i))

                if self.request.GET.get('mpe'):
                    t_obj = t_obj.filter(Maximum_Education_Level__lte=self.request.GET.get('mpe'))

                if self.request.GET.get('mpel'):
                    t_obj = t_obj.filter(Maximum_Education_Level__gte=self.request.GET.get('mpel'))

                if self.request.GET.get('run'):
                    t_obj = t_obj.filter(Education_Medium=self.request.GET.get('run'))

                if self.request.GET.get('medium'):
                    t_obj = t_obj.filter(Education_Medium=self.request.GET.get('medium'))

                if self.request.GET.get('gender'):
                    t_obj = t_obj.filter(Gender=self.request.GET.get('gender'))

                if self.request.GET.get('type'):
                    t_obj = t_obj.filter(Type=self.request.GET.get('type'))

                # Experience filter+++
                # location filter
                # Rating sort filter (max-min)
                # RatedPerson sort  filter (Max-min)
                # has Certificate
                # has Nid
                # has any reminder
                return t_obj.order_by('-Rating')
            else:
                c_obj = Child.objects.get(slug=self.request.GET['child'])
                t_obj = Teacher.objects.all()
                g_obj_list = GuardianDetails.objects.all()
                g_obj = GuardianDetails.objects.first()
                for i in g_obj_list:
                    for j in i.Child.all():
                        if c_obj.slug == j.slug:
                            g_obj = i

                addr1ess = g_obj.Address.split(',')
                addr1 = addr1ess[0]
                addr2 = addr1ess[1]
                addr3 = addr1ess[-1]
                addr4 = addr1ess[-2]

                # if c_obj.Teacher_Gender != 4:
                #     t_obj = Teacher.objects.filter(Q(Gender=c_obj.Teacher_Gender) &
                #                                    Q(Maximum_Education_Level__gte=c_obj.Education_Level) &
                #                                    Q(BAN=False) & (
                #                                            Q(Location0__icontains=addr1) |
                #                                            Q(Location0__icontains=addr2) |
                #                                            Q(Location0__icontains=addr3) |
                #                                            Q(Location0__icontains=addr4) |
                #
                #                                            Q(Location1__icontains=addr1) |
                #                                            Q(Location1__icontains=addr2) |
                #                                            Q(Location1__icontains=addr3) |
                #                                            Q(Location1__icontains=addr4) |
                #
                #                                            Q(Location2__icontains=addr1) |
                #                                            Q(Location2__icontains=addr2) |
                #                                            Q(Location2__icontains=addr3) |
                #                                            Q(Location2__icontains=addr4) |
                #
                #                                            Q(Location3__icontains=addr1) |
                #                                            Q(Location3__icontains=addr2) |
                #                                            Q(Location3__icontains=addr3) |
                #                                            Q(Location3__icontains=addr4) |
                #
                #                                            Q(Location4__icontains=addr1) |
                #                                            Q(Location4__icontains=addr2) |
                #                                            Q(Location4__icontains=addr3) |
                #                                            Q(Location4__icontains=addr4)
                #                                    ) & (
                #                                            Q(Running_Tuition=False) |
                #                                            Q(Rating__isnull=False)
                #                                    ))
                # else:
                #     t_obj = Teacher.objects.filter(Q(Maximum_Education_Level__gte=c_obj.Education_Level) &
                #                                    Q(BAN=False) & (
                #                                            Q(Location0__icontains=addr1) |
                #                                            Q(Location0__icontains=addr2) |
                #                                            Q(Location0__icontains=addr3) |
                #                                            Q(Location0__icontains=addr4) |
                #
                #                                            Q(Location1__icontains=addr1) |
                #                                            Q(Location1__icontains=addr2) |
                #                                            Q(Location1__icontains=addr3) |
                #                                            Q(Location1__icontains=addr4) |
                #
                #                                            Q(Location2__icontains=addr1) |
                #                                            Q(Location2__icontains=addr2) |
                #                                            Q(Location2__icontains=addr3) |
                #                                            Q(Location2__icontains=addr4) |
                #
                #                                            Q(Location3__icontains=addr1) |
                #                                            Q(Location3__icontains=addr2) |
                #                                            Q(Location3__icontains=addr3) |
                #                                            Q(Location3__icontains=addr4) |
                #
                #                                            Q(Location4__icontains=addr1) |
                #                                            Q(Location4__icontains=addr2) |
                #                                            Q(Location4__icontains=addr3) |
                #                                            Q(Location4__icontains=addr4)
                #                                    ) & (
                #                                            Q(Running_Tuition=False) |
                #                                            Q(Rating__isnull=False)
                #                                    ))
                #
                #     # for i in c_obj.Teacher_University.all():
                #     #     t_obj |= t_obj.filter(Q(Graduation_Institute=i))
                return t_obj.order_by('-Rating')
        except:
            return Teacher.objects.all()


class ChildUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = ChildSerializer
    queryset = Child.objects.all()
    lookup_field = 'pk'


class ChildRetriveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = ChildSerializerRetrive
    queryset = Child.objects.all()
    lookup_field = 'pk'


# Teacher section


class TeacherDetailsListView(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherDetailsSerializer


class TeacherDetailsView(RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Teacher.objects.all()
    serializer_class = TeacherDetailsSerializer


class TeacherHistoryView(ListAPIView):
    lookup_field = 'pk'
    serializer_class = TeacherHistorySerializer

    def get_queryset(self):
        return TeacherHistory.objects.filter(Teacher_id=self.kwargs['pk'])


# FollowUp original view
class FollowUpView(TemplateView):
    template_name = 'FollowUp/index.html'


class FollowUpPaid(TemplateView):
    template_name = 'FollowUp/permanent_tuition_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = PermanentTuitionForChild.objects.all()
        obj = obj.filter(Child__Paid=True, Child__Canceled=False).order_by('date')
        context['childs'] = obj
        print(obj)
        return context


class FollowUpConfirm(TemplateView):
    template_name = 'FollowUp/permanent_tuition_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = PermanentTuitionForChild.objects.all()
        obj = obj.filter(Child__Paid=False, Child__Canceled=False).order_by('date')
        context['childs'] = obj
        print(obj)
        return context


class FollowUpAssign(TemplateView):
    template_name = 'FollowUp/sorted_tuition_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = DemoTeacherForChild.objects.all()
        obj = obj.filter(Child__Paid=False, permanent=False, Child__Canceled=False)
        context['childs'] = obj
        print(obj)
        return context


class FollowUpCanceled(TemplateView):
    template_name = 'FollowUp/sorted_tuition_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = PermanentTuitionForChild.objects.all()
        obj = obj.filter(Child__Canceled=True).order_by('date')
        context['childs'] = obj
        print(obj)
        return context


class FollowUpGuardianTableView(TemplateView):
    template_name = 'FollowUp/guardian-table.html'


class FollowUpTuitionTableView(TemplateView):
    template_name = 'FollowUp/portal.html'


class SendSMSView(TemplateView):
    template_name = 'FollowUp/sms.html'


class ReminderView(TemplateView):
    template_name = 'FollowUp/reminders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            time_str = self.request.GET.get('date').split('-')
            context['reminders'] = Reminder.objects.filter(Time__day=int(time_str[2]), Time__month=int(time_str[1]),
                                                           Time__year=int(time_str[0])).filter(
                User=self.request.user).order_by('Time')
            return context
        except:
            time_str = str(datetime.date.today()).split('-')
            context['reminders'] = Reminder.objects.filter(Time__day=int(time_str[2]), Time__month=int(time_str[1]),
                                                           Time__year=int(time_str[0])).filter(
                User=self.request.user).order_by('Time') | \
                                   Reminder.objects.filter(User=self.request.user)
            return context


class AddRating(APIView):
    def get(self, request):
        try:
            if request.GET.get('tid'):
                if request.GET.get('rtn'):
                    tobj = Teacher.objects.get(id=request.GET.get('tid'))
                    tobj.Rating = request.GET.get('rtn')
                    tobj.RatedPerson = tobj.RatedPerson + 1
                    tobj.save()
                    return Response({'rating': str(tobj.Rating)})
            elif request.GET.get('gid'):
                if request.GET.get('rtn'):
                    gobj = GuardianDetails.objects.all()
                    gobj.RatedPerson = gobj.RatedPerson + 1
                    gobj.Rating = request.GET.get('rtn')
                    gobj.save()
                    return Response({'rating': str(gobj.Rating)})
            else:
                return Response({'rating': 'Something not valid'})
        except Exception as e:
            return Response({'rating': str(e)})


class SendSMSViewtest(TemplateView):
    template_name = 'FollowUp/sms2.html'


class SetPaid(GenericAPIView):
    def get(self, request):
        tip = PermanentTuitionForChild.objects.get(Child_id=self.request.GET.get('id'))
        ch = Child.objects.get(slug=tip.Child.slug)
        ch.active = False
        ch.Paid = True
        ch.save()
        tip.paid = True
        tip.save()
        return Response({'Paid': True})


class RoughNoteAdd(GenericAPIView):
    def get(self, request):
        try:
            note_obj = RoughNote.objects.create(Child_id=self.request.GET.get('cid'),
                                                user=get_current_user(),
                                                Text='Guardian' + ' : ' + self.request.GET.get(
                                                    'talk'))
            note_obj.save()
        except Exception as e:
            return Response({'Error': str(e)})
        return Response({'ok': 'ok'})


class NoteAdd(GenericAPIView):
    def get(self, request):
        try:
            if self.request.GET.get('c') == '1':  # Reserve note
                obj = TemporaryTuitionForChild(Child_id=self.request.GET.get('cid'))
                obj.TalksJson[self.request.GET.get('tid')] = [str(
                    obj.TalksJson[self.request.GET.get('tid')]) + ' > ' + self.request.GET.get('talk'),
                                                              str(datetime.date.today())]
                obj.save()
            elif self.request.GET.get('c') == '2':  # Shorlist note
                obj = ShortListedTuitionForChild(Child_id=self.request.GET.get('cid'))
                obj.TalksJson[self.request.GET.get('tid')] = [str(
                    obj.TalksJson[self.request.GET.get('tid')]) + ' > ' + self.request.GET.get('talk'),
                                                              str(datetime.date.today())]
                obj.save()
            elif self.request.GET.get('c') == '3':  # Assigned note
                obj = AssignedTeacherForChild(Child_id=self.request.GET.get('cid'))
                obj.TalksJson[self.request.GET.get('tid')] = [str(
                    obj.TalksJson[self.request.GET.get('tid')]) + ' > ' + self.request.GET.get('talk'),
                                                              str(datetime.date.today())]
                obj.save()
            elif self.request.GET.get('c') == '4':  # Demo note
                obj = DemoTeacherForChild(Child_id=self.request.GET.get('cid'))
                obj.TalksJson[self.request.GET.get('tid')] = [str(
                    obj.TalksJson[self.request.GET.get('tid')]) + ' > ' + self.request.GET.get('talk'),
                                                      str(datetime.date.today())]
                obj.save()
            else:
                return Response({'Section': 'No section selected'})
            return Response({'Talk': self.request.GET.get('talk'), 'Teacher': self.request.GET.get('tid')})
        except Exception as e:
            return Response({'Error': str(e)})
