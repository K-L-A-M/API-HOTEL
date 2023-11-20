# views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from users.permissions import IsEmployeeOrManagerOrAdministratorPermission
from users.serializers import UserSerializer
from .models import User
from rest_framework import generics


class TokenObtainpairView(TokenObtainPairView):
    ...


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(
        description="Route for User Creation",
        tags=["User Creation"],
        parameters=[
            UserSerializer,
        ],
    )
    def post(self, request):
        return self.create(request)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsEmployeeOrManagerOrAdministratorPermission]

    @extend_schema(
        description="Route for User Listing",
        tags=["User Listing"],
        parameters=[
            UserSerializer,
        ],
    )
    def get(self, request, *args, **kwargs):

        if not IsEmployeeOrManagerOrAdministratorPermission().has_permission(request, self):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        return super().list(request, *args, **kwargs)
