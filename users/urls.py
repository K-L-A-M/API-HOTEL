# users/urls.py
from django.urls import path
from users.views import TokenObtainpairView, UserCreateView, UserListView

urlpatterns = [
    path("users/", UserCreateView.as_view()),
    path("users/", UserListView.as_view()),
    path('login/', TokenObtainpairView.as_view(), name='token_obtain_pair'),
]
