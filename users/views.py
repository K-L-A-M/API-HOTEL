# views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from users.permissions import IsEmployeeOrManagerOrAdministratorPermission
from users.serializers import UserSerializer
from .models import TypeUser, User
from rest_framework import generics


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)

            refresh = RefreshToken.for_user(user)
            token = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'email': user.email,
                'user_type': user.user_type,
                'user_id': user.id,
            }

            if user.user_type == TypeUser.ADMIN:
                token['admin_token'] = True
            elif user.user_type == TypeUser.USER:
                token['user_token'] = True
            elif user.user_type == TypeUser.EMPLOYEE:
                token['employee_token'] = True
            elif user.user_type == TypeUser.MANAGER:
                token['manager_token'] = True

            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


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
    def list(self, request, *args, **kwargs):

        if not IsEmployeeOrManagerOrAdministratorPermission().has_permission(request, self):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        return super().list(request, *args, **kwargs)
