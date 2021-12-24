import datetime
import socket
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from FollowUp.models import SMS, EmployeeLoginHistory, Teacher


from django.contrib.auth.signals import user_logged_in, user_logged_out

def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return User.objects.filter(id__in=user_id_list)


class CurrentUser(APIView):
    def get(self, request):
        print(get_current_users())
        return Response({'Response':str(get_current_users())})


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    # success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserRedirect(APIView):
    def get(self, request):
        try:
            print(request.user.is_Guardian)
            if self.request.user.is_FollowUpper:
                return redirect('/follow/')
            elif request.user.is_Teacher:
                teacher_obj = Teacher.objects.get(auth=request.user)
                return redirect('/teacher/update/' + str(teacher_obj.id))
            elif request.user.is_Guardian:
                return redirect('/guardian/profile/')
            else:
                return redirect('/api-auth/login/')
        except:
            return redirect('/api-auth/login/')


class SendSMS(APIView):
    def get(self, request):
        HOST = '127.0.0.1'  # The server's hostname or IP address
        PORT = 9994  # The port used by the server

        if request.GET.get('phone'):
            print(request.GET.get('phone'))
            if request.GET.get('text'):
                print(request.GET.get('text'))
                text = request.GET.get('text').replace("'", "`")
                sms = request.GET.get('phone') + '::' + text
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.send(sms.encode())
                    data = s.recv(1024)
                    d = SMS(sender=request.user, number=request.GET.get('phone'), text=request.GET.get('text'))
                    d.save()
                    print(data)
        return Response({'ok': 'ok'})


def add_login_time(sender, user, request, **kwargs):
    try:
        if user.is_staff:
            EmployeeLoginHistory.objects.get(Q(Date=datetime.datetime.now()) & Q(User=user))
        pass
    except:
        if user.is_staff:
            obj = EmployeeLoginHistory(User=user, Login=datetime.datetime.now())
            obj.save()


def add_logout_time(sender, user, request, **kwargs):
    try:
        if user.is_staff:
            obj = EmployeeLoginHistory.objects.get(Q(Date=datetime.datetime.now()) & Q(User=user))
            obj.Logout = datetime.datetime.now()
            obj.save()
    except:
        pass


user_logged_in.connect(add_login_time)
user_logged_out.connect(add_logout_time)