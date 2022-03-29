from django.urls import path
from . import views

urlpatterns = [
    path('help/', views.index, name='help'),
    path('help/notice/post_notice', views.post_notice, name='post_notice'),
    path('help/notice/', views.notice, name='notice'),
    path('help/notice/edit/<int:id>', views.edit_notice, name='edit_notice'),
    path('noice/delete_notice/<int:id>', views.delete_notice, name="delete_notice"),
    path('help/review/', views.review, name='review'),
    path('help/review/new', views.post_review, name='post_review'),
    path('help/review/delete/<int:id>', views.delete_review, name='del_review'),
    path('help/review/update/<int:id>', views.update_review, name='update-review'),

]
