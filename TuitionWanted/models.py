from django.conf import settings
from django.db import models
from django .contrib.auth.models import AbstractUser
User = settings.AUTH_USER_MODEL

# Model to store the list of logged in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user')
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username