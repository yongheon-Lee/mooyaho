from django.urls import path
from . import views

urlpatterns = [
    path('help/', views.index, name='help'),
    path('help/notice/post_notice', views.post_notice, name='post_notice'),
    path('help/notice/', views.notice, name='notice'),
    # path('noice/delete/<int:id>', views.delete_notice, name="delete_notice"),
    path('help/review/', views.review, name='review'),
    path('help/review/new', views.post_review, name='post_review'),
]
