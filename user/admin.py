from django.contrib import admin

from .user_models import MooyahoUser, UserViewLog

admin.site.register(MooyahoUser)
admin.site.register(UserViewLog)
