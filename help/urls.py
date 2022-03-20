from django.urls import path
from . import views

urlpatterns = [
    path('help/', views.index, name='help'),
    path('notice/', views.notice, name='notice'),
    path('review/', views.review, name='review'),
]
