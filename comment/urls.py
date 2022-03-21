from django.urls import path

from . import comment_service

urlpatterns = [
    path('posts/<int:pk>/comments/', comment_service.comment, name='comment'),
]
