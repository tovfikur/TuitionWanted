from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, GenericAPIView
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.http import JsonResponse
from .models import Teacher, Subject, TEACHING_LEVEL_CHOICE, TEACHING_MEDIUM_CHOICE, TeachingSection, \
    Areas, University, Division, District, Thana, ClassesSubject, Schools
from .form import TeacherRegistrationForm
from .serializers import TeacherListSerializers, SubjectSerializers, TeacherListCreateSerializers, \
    TeachingSectionAPI, AreasSerializers, DistrictSerializer, DivisionSerializer, ThanaSerializer
from django.contrib.auth import authenticate, login
from django.utils.safestring import mark_safe


def nested_tuple_text(index, x):
    for i in x:
        if i[0] == index:
            return i[1]


# Api View


class DivisionApi(ListAPIView):
    pagination_class = None
    serializer_class = DivisionSerializer
    queryset = Division.objects.all()


class DistrictApi(ListAPIView):
    pagination_class = None
    serializer_class = DivisionSerializer

    def get_queryset(self):
        return District.objects.filter(Division_id=self.request.GET.get('id'))


class ThanaApi(ListAPIView):
    pagination_class = None
    serializer_class = DivisionSerializer

    def get_queryset(self):
        return Thana.objects.filter(District_id=self.request.GET.get('id'))


class TeacherClassApi(GenericAPIView):
    def get(self, request):
        return Response(TEACHING_LEVEL_CHOICE)


class TeacherMediumApi(GenericAPIView):
    def get(self, request):
        return Response(TEACHING_MEDIUM_CHOICE)


class AddNationalUniversity(GenericAPIView):
    def get(self, request):
        try:
            if request.GET.get('name'):
                versity_obj = University.objects.create(Name=request.GET.get('name'), Category=2)
                versity_obj.save()
            else:
                return Response({'university': 13})
            return Response({'university': versity_obj.id})
        except Exception as e:
            return Response({'error': str(e)})


class TeacherSubjectApi(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializers
    pagination_class = None


class TeacherAreasApi(ListAPIView):
    queryset = Areas.objects.all()
    serializer_class = AreasSerializers
    pagination_class = None


class TeacherExperienceApi(ListAPIView):
    serializer_class = TeachingSectionAPI
    pagination_class = None

    def get_queryset(self):
        try:
            return Teacher.objects.get(id=self.request.GET.get('id')).Experience.all()
        except Exception as e:
            return Response({'error': str(e)})


class TeacherRemoveSubjectApi(GenericAPIView):
    def get(self, request):
        try:
            if request.GET.get('id'):
                teaching_obj = TeachingSection.objects.get(id=request.GET.get('id'))
                teaching_obj.delete()
                return Response({'delete': 'success'})
        except Exception as e:
            return Response({'error': str(e)})
            pass


class TeacherAddSubjectApi(GenericAPIView):

    def get(self, request):
        try:
            if request.GET.get('id'):
                class_value = int(request.GET.get('class'))
                medium_value = int(request.GET.get('medium'))
                subject_value = request.GET.get('subject')
                teacher_obj = Teacher.objects.get(id=request.GET.get('id'))
                teaching_obj = TeachingSection.objects.create(
                    Preferred_Education=int(class_value),
                    Preferred_Medium=int(medium_value),
                )
                subject_string = ''
                for i in subject_value.split(','):
                    teaching_obj.Preferred_Subject.add(int(i))
                    subject_string = subject_string + Subject.objects.get(id=int(i)).Title + ', '
                teaching_obj.save()
                if int(request.GET.get('exp')):
                    teacher_obj.Experience.add(teaching_obj)
                else:
                    teacher_obj.Preferred.add(teaching_obj)
                teacher_obj.save()

                return Response({'id': teaching_obj.id, 'class': nested_tuple_text(class_value, TEACHING_LEVEL_CHOICE),
                                 'medium': nested_tuple_text(medium_value, TEACHING_MEDIUM_CHOICE),
                                 'subject': subject_string})

        except Exception as e:
            return Response({'error': str(e)})
            pass


class TeacherListApi(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherListSerializers


class TeacherCreateApi(CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherListCreateSerializers


class TeacherUpdateApi(RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Teacher.objects.all()
    serializer_class = TeacherListCreateSerializers


class TeacherProfileView(TemplateView):
    template_name = 'Teacher/profile.html'

    def get_context_data(self, **kwargs):
        try:
            return {"userd": Teacher.objects.get(id=self.request.GET.get('id'))}
        except:
            return {
                "userd": Teacher.objects.get(id=2000)
            }


class TeacherRegistrationView(FormView):
    form_class = TeacherRegistrationForm
    template_name = 'Teacher/registration.html'


class TeacherUpdateView(UpdateView):
    model = Teacher

    def get_template_names(self):
        if 'mobile' in str(self.request.META['HTTP_USER_AGENT']).lower():
            return 'Teacher/update_mobile.html'
        return 'Teacher/update.html'
        # return 'Teacher/update_mobile.html'

    form_class = TeacherRegistrationForm

    def get_context_data(self, **kwargs):
        if str(Teacher.objects.get(id=str(self.request.path).replace('/teacher/update/', '')).auth) == str(
                self.request.user):
            context = super(TeacherUpdateView, self).get_context_data(**kwargs)

            try:
                stri = []
                for i in Schools.objects.all():
                    stri.append(i.Name)

                context['schools'] = stri
            except:
                pass

            try:
                obj = Teacher.objects.get(id=str(self.request.path).replace('/teacher/update/', ''))
                PermanentLocaton = str(obj.PermanentLocationThana) + str(obj.PermanentLocationDistrict) + str(
                    obj.PermanentLocationDivision)
                context['PermanentLocaton'] = PermanentLocaton + ', '
            except:
                context['PermanentLocaton'] = ''

            try:

                obj = Teacher.objects.get(id=str(self.request.path).replace('/teacher/update/', ''))
                PresentLocation = str(obj.PresentLocationThana) + str(obj.PresentLocationDistrict) + str(
                    obj.PresentLocationDivision)
                context['PresentLocation'] = PresentLocation + ', '
            except:
                context['PresentLocation'] = ''

            try:
                strin = ''
                for i in Teacher.objects.get(
                        id=str(self.request.path).replace('/teacher/update/', '')).PreferredArea.all():
                    strin = '<option onclick="AddPrefArea(this, ' + str(i.id) + ',\'' + str(
                        i.Name) + '\')" value="440">' + str(i.Name) + '</option>'
                context['PrefArea'] = mark_safe(strin)
            except Exception as e:
                print(e)
                context['PrefArea'] = ''

            try:
                strin = ''
                for i in Teacher.objects.get(
                        id=str(self.request.path).replace('/teacher/update/', '')).Experience.all():
                    strin = strin + '<div><i class="fas fa-window-close fa-2x" onclick = "delete_teaching_section_selected(\'' + str(
                        i.id) + '\', this, 1)" ></i> &nbsp;' + str(i) + '</div><br>'
                context['Experience'] = mark_safe(strin)
            except Exception as e:
                print(e)
                context['Experience'] = ''

            try:
                strin = ''
                for i in Teacher.objects.get(id=str(self.request.path).replace('/teacher/update/', '')).Preferred.all():
                    strin = strin + '<div><i class="fas fa-window-close fa-2x" onclick = "delete_teaching_section_selected(\'' + str(
                        i.id) + '\', this, 1)" ></i> &nbsp;' + str(i) + '</div><br>'
                context['Preferred'] = mark_safe(strin)
            except:
                context['Preferred'] = ''

            try:
                context['Avatar_url'] = Teacher.objects.get(
                    id=str(self.request.path).replace('/teacher/update/', '')).get_avatar()
            except:
                context[
                    'Avatar_url'] = 'https://www.pinclipart.com/picdir/middle/499-4992513_avatar-avatar-png-clipart.png'
            try:
                context['StudentID_url'] = Teacher.objects.get(
                    id=str(self.request.path).replace('/teacher/update/', '')).StudentID.url
            except:
                context[
                    'StudentID_url'] = 'https://image.shutterstock.com/image-vector/student-id-card-university-school-260nw-1420220018.jpg'
            try:
                context['Certificate_url'] = Teacher.objects.get(
                    id=str(self.request.path).replace('/teacher/update/', '')).Certificate.url
            except:
                context['Certificate_url'] = '/media/unnamed.jpg'
            try:
                context['NID_url'] = Teacher.objects.get(
                    id=str(self.request.path).replace('/teacher/update/', '')).NID.url
            except:
                context['NID_url'] = '/media/nid.jpg'
            return context
        else:
            return {"no": "no"}


class logmein(GenericAPIView):
    def get(self, request):
        username = request.GET.get('username')
        password = request.GET.get('pwd')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'login': True})
        else:
            return Response({'login': False})


class SubjectClassView(ListAPIView):
    serializer_class = SubjectSerializers
    pagination_class = None

    def get_queryset(self):
        try:
            level = ClassesSubject.objects.filter(Class=self.request.GET.get('level')).filter(
                Medium=self.request.GET.get('medium')).first()
            objs = level.Subject.all()
            return objs
        except Exception as e:
            return Subject.objects.all()
