from django.urls import path

from . import comment_service

urlpatterns = [
    # path('posts/<int:pk>/comments/', comment_service.new_comment, name='comment'),
    path('comments/', comment_service.new_comment, name='comment'),
]
