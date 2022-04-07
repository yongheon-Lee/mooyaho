from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import user_service

urlpatterns = [
    path('login/', user_service.login, name='login'),
    path('signup/', user_service.signup, name='signup'),
    path('signup/doublecheck/', user_service.duplication_check, name='duplication_check'),
    path('logout/', user_service.logout, name='logout'),
    path('mypage/', user_service.my_page, name='mypage'),
    path('delete-account/', user_service.delete_account, name='delete-account'),
]
# + static(settings.USER_MEDIA_URL, document_root=settings.USER_MEDIA_ROOT)
