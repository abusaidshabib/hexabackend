from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserRegisterSerializer, UserLoginSerializer

# Create your views here.


class RegisterAPIView(APIView):
    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"success": True, "message": "User creation done", "data": user}, status=status.HTTP_201_CREATED)
        return Response(
            {"success": False, "message": "Validation failed",
                "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginAPIView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"success": False, "message": "Invalid credentials",
                 "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            "success": True,
            "message": "User login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)