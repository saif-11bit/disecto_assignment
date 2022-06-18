from django.contrib import admin
from .models import Consultant, Visitor, User, WorkingPeriod

admin.site.register(User)
admin.site.register(Consultant)
admin.site.register(Visitor)
admin.site.register(WorkingPeriod)
