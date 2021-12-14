from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url, re_path
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import CurrentUser, SignUpView, UserRedirect, SendSMS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/accounts/profile/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('guardian/', include('GuardianArea.urls')),
    path('teacher/', include('Teacher.urls')),
    path('follow/', include('FollowUp.urls')),
    path('user/', CurrentUser.as_view()),
    path('', UserRedirect.as_view()),
    path('accounts/profile/', UserRedirect.as_view()),
    re_path('accounts/login/', UserRedirect.as_view()),
    path('send_sms/', login_required(SendSMS.as_view())),
    url(r'^signup/$', SignUpView.as_view()),
    url(r'^advanced_filters/', include('advanced_filters.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Tuition Wanted"
admin.site.site_title = "Tuition Wanted"
admin.site.index_title = "Tuition Wanted Portal"
