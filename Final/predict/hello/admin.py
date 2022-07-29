from atexit import register
from django.contrib import admin
from .models import Contact
from .models import Reply
# Register your models here.

admin.site.register(Contact)
admin.site.register(Reply)