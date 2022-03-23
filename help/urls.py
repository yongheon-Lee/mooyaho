from django.urls import path
from . import views

urlpatterns = [
    path('help/', views.index, name='help'),
    path('post_notice', views.post_notice, name='post_notice'),
    path('notice/', views.notice, name='notice'),
    path('noice/delete/<int:id>', views.delete_notice, name="delete_notice"),
    path('review/', views.review, name='review'),
]
