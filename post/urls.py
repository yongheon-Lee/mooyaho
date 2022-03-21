from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import post_service, comment_service

urlpatterns = [
    path('posts/', post_service.post_list, name='posts'),
    path('posts/<int:pk>/', post_service.post_detail, name='posts-detail'),
    path('posts/new/', post_service.post, name='posts-new'),
    path('posts/<int:pk>/comments/', comment_service.comment, name='comment'),
]
# + static(settings.POST_MEDIA_URL, document_root=settings.POST_MEDIA_ROOT)
