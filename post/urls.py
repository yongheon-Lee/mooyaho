from django.urls import path

from . import post_service

urlpatterns = [
    path('posts/', post_service.post_list, name='posts'),
    path('posts/<int:pk>/', post_service.post_detail, name='posts-detail'),
    path('posts/new/', post_service.post, name='posts-new'),
    path('posts/<int:pk>/edition/', post_service.edit_post, name='posts-change'),
    path('posts/<int:pk>/deletion/', post_service.delete_post, name='posts-delete')
]
# + static(settings.POST_MEDIA_URL, document_root=settings.POST_MEDIA_ROOT)
