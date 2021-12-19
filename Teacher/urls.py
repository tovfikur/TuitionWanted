from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import TeacherListApi, TeacherProfileView, \
    TeacherRegistrationView, TeacherCreateApi, TeacherUpdateApi, \
    TeacherUpdateView, TeacherClassApi, TeacherMediumApi, TeacherSubjectApi, TeacherAddSubjectApi, \
    TeacherExperienceApi, TeacherAreasApi, TeacherRemoveSubjectApi, AddNationalUniversity, logmein, \
    DistrictApi, DivisionApi, ThanaApi, SubjectClassView

urlpatterns = [
    path('api/list', TeacherListApi.as_view()),
    path('api/logmein', logmein.as_view()),
    path('view/', TeacherProfileView.as_view()),
    path('registration/', TeacherRegistrationView.as_view()),
    path('api/registration/', TeacherCreateApi.as_view()),
    path('api/update/addxp', login_required(TeacherAddSubjectApi.as_view())),
    path('api/update/delxp', login_required(TeacherRemoveSubjectApi.as_view())),
    path('api/update/<pk>', login_required(TeacherUpdateApi.as_view())),
    path('api/add/university', login_required(AddNationalUniversity.as_view())),
    path('api/class/', TeacherClassApi.as_view()),
    path('api/class/subject/', SubjectClassView.as_view()),
    path('api/medium/', TeacherMediumApi.as_view()),
    path('api/subject/', TeacherSubjectApi.as_view()),
    path('api/experience/', TeacherExperienceApi.as_view()),
    path('api/areas/', TeacherAreasApi.as_view()),
    path('api/areas/district/', DistrictApi.as_view()),
    path('api/areas/division/', DivisionApi.as_view()),
    path('api/areas/thana/', ThanaApi.as_view()),
    path('update/<pk>', login_required(TeacherUpdateView.as_view())),
]
