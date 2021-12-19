from django.urls import path, include
from .views import (GuardianView, TemporaryTeacherView, NoteCreateView, GuardianProfile, ChildProfile,\
    GuardianRegistrationView, GuardianCreateView, GuardianProfileView, ChildAddView, ChildCreateView, GuardianLoginView)
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('teacher/', TemporaryTeacherView.as_view()),
    path('create/', GuardianCreateView.as_view()),
    path('create/child', ChildCreateView.as_view()),
    path('api/note_create/', NoteCreateView.as_view()),
    path('register/', GuardianRegistrationView.as_view()),
    path('login/', GuardianLoginView.as_view()),
    path('register/child', ChildAddView.as_view()),
    path('profile/', GuardianProfileView.as_view()),
    path('<id>/', GuardianView.as_view()),
    path('<id>/profile/', login_required(GuardianProfile.as_view())),
    path('<id>/child/', login_required(ChildProfile.as_view())),
]