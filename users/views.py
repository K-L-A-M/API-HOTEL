# views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from .models import TypeUser


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
