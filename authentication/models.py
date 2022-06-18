from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    is_consultant = models.BooleanField(default=False)
    is_visitor = models.BooleanField(default=False)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token),
        }
        

class Consultant(models.Model):
    STATUS = (
        ('ONLINE', 'ONLINE'),
        ('OFFLINE', 'OFFLINE'),
        ('BUSY', 'BUSY'),
    )
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True, related_name='consultant')
    status = models.CharField(choices=STATUS, default='OFFLINE',max_length=100)
    
    def __str__(self):
        return self.user.username


class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True, related_name='visitor')
    
    def __str__(self):
        return self.user.username


class WorkingPeriod(models.Model):
    consultant = models.ForeignKey(Consultant, on_delete=models.PROTECT, related_name="working_period")
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.consultant.user.username
