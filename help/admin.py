from django.contrib import admin

# Register your models here.
from help.models import Notice, Review

admin.site.register(Notice)
admin.site.register(Review)
