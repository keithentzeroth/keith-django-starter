from mysite.polls.models import Poll
from django.contrib import admin
from mysite.polls.models import Choice

admin.site.register(Poll)
admin.site.register(Choice)
