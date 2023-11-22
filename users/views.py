# views.py
import uuid
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from users.permissions import IsEmployeeOrManagerOrAdministratorPermission, IsOwnerOrEmployeeOrManagerOrAdministratorPermission
from users.serializers import UserSerializer
from .models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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
    permission_classes = [IsAuthenticated, IsEmployeeOrManagerOrAdministratorPermission]

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


class UserRetrieveDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsEmployeeOrManagerOrAdministratorPermission]

    @extend_schema(
        description="Route for User Retrive and Deletion",
        tags=["User Retrive and Deletion"],
        parameters=[
            UserSerializer,
        ],
    )
    def get_object(self):
        user_id = self.kwargs['id']
        user_id = uuid.UUID(user_id.replace("-", ""))
        return get_object_or_404(User, id=user_id)

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.check_object_permissions(request, self.get_object())
        return super().destroy(request, *args, **kwargs)


class UserEditView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrEmployeeOrManagerOrAdministratorPermission | IsEmployeeOrManagerOrAdministratorPermission]

    @extend_schema(
        description="Route for User Editing",
        tags=["User Editing"],
        parameters=[
            UserSerializer,
        ],
    )
    def get_object(self):
        user_id = self.kwargs.get("id")
        if user_id:
            try:
                user_id = uuid.UUID(user_id.replace("-", ""))
                return get_object_or_404(User, id=user_id)
            except ValueError:
                return None
        else:
            return None

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user:
            self.check_object_permissions(request, user)

            if self.request.method == 'PATCH' or 'PUT':
                partial = True
            else:
                partial = False

            serializer = self.get_serializer(user, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'UUID inválido'}, status=status.HTTP_400_BAD_REQUEST)
