# users/urls.py
from django.urls import path, re_path
from users.views import TokenObtainpairView, UserCreateView, UserListView, UserRetrieveDestroy, UserEditView

urlpatterns = [
    path("users/", UserCreateView.as_view()),
    path("users/list/", UserListView.as_view()),
    re_path(r'users/(?P<id>[a-fA-F0-9]{32,36})/$', UserRetrieveDestroy.as_view(), name='user-detail'),
    re_path(r'users/edit/(?P<id>[a-fA-F0-9]{32,36})/$', UserEditView.as_view(), name='user-detail'),
    path('login/', TokenObtainpairView.as_view(), name='token_obtain_pair'),
]
