from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
# models
from .models import Child, GuardianDetails, Note
from Teacher.models import Teacher
from FollowUp.models import PermanentTuitionForChild, TemporaryTuitionForChild, ShortListedTuitionForChild, \
    AssignedTeacherForChild, DemoTeacherForChild

# serializers
from .serializers import GuardianListSerializers, NoteSerializers, ChildSerializer


class GuardianView(RetrieveAPIView):
    serializer_class = GuardianListSerializers
    queryset = GuardianDetails.objects.all()
    lookup_field = 'id'


class GuardianCreateView(CreateAPIView):
    serializer_class = GuardianListSerializers
    queryset = GuardianDetails
    lookup_field = 'id'


class ChildCreateView(CreateAPIView):
    serializer_class = ChildSerializer
    queryset = Child
    lookup_field = 'id'


class TemporaryTeacherView(APIView):

    def get(self, request):
        return Response({'this': 'that'})


class NoteCreateView(ListCreateAPIView):
    serializer_class = NoteSerializers
    queryset = Note.objects.all()
    pagination_class = None


class GuardianProfile(TemplateView):
    template_name = 'GuardianArea/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(GuardianProfile, self).get_context_data(**kwargs)
        try:
            gobj = GuardianDetails.objects.get(id=self.kwargs['id'])
            c = 0
            # for i in gobj.Child.all():
            #     # context['child'][c] = i
            #     c += 1
            context['child'] = gobj.Child.all()
            context['guardian'] = gobj
        except:
            pass
        return context


class ChildProfile(TemplateView):
    template_name = 'GuardianArea/child-profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ChildProfile, self).get_context_data(*args, **kwargs)
        try:
            cobj = Child.objects.get(slug=self.kwargs['id'])
            context['child'] = cobj
            self.request.session['child_id'] = cobj.slug
        except:
            pass

        # get temporary teacher

        try:
            temp_tobj = TemporaryTuitionForChild.objects.get(Child_id=self.kwargs['id'])
            context['temporary'] = temp_tobj
        except:
            pass

        try:
            temp_tobj = ShortListedTuitionForChild.objects.get(Child_id=self.kwargs['id'])
            context['short'] = temp_tobj
        except:
            pass

        try:
            temp_tobj = AssignedTeacherForChild.objects.get(Child_id=self.kwargs['id'])
            context['assign'] = temp_tobj
        except:
            pass

        try:
            temp_tobj = DemoTeacherForChild.objects.get(Child_id=self.kwargs['id'])
            context['demo'] = temp_tobj
        except:
            pass

        try:
            temp_tobj = PermanentTuitionForChild.objects.get(Child_id=self.kwargs['id'])
            context['permanent'] = temp_tobj
        except:
            pass

        try:
            temp_tobj = GuardianDetails.objects.get(Child__slug=self.kwargs['id'])
            context['guardian'] = temp_tobj
        except:
            pass

        try:
            temp_tobj = Note.objects.all()
            context['notes'] = temp_tobj
        except:
            pass
        return context


class GuardianRegistrationView(TemplateView):
    template_name = 'GuardianArea/registration.html'


class GuardianLoginView(TemplateView):
    template_name = 'GuardianArea/login.html'



class ChildAddView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(ChildAddView, self).get_context_data(**kwargs)
        context['guardian'] = GuardianDetails.objects.get(auth=self.request.user)
        return context
    template_name = 'GuardianArea/client-child-add.html'


class GuardianProfileView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(GuardianProfileView, self).get_context_data(**kwargs)
        context['guardian'] = GuardianDetails.objects.get(auth=self.request.user)
        return context

    template_name = 'GuardianArea/client-profile.html'
