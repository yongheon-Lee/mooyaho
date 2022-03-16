from django.urls import path
from . import views

urlpatterns = [
    path('mountains/', views.mountains, name='mountains'),
    path('mountains_detail/<int:id>/', views.mountains_detail, name='mountains_detail'),
]