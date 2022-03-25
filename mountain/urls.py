from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main'),
    path('mountains/', views.mountains, name='mountains'),
    path('mountains_detail/<int:id>/', views.mountains_detail, name='mountains_detail'),
    path('get-mountain-list/', views.mountain_list, name='mountain_list'),
]