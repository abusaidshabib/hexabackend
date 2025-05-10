from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserRegisterSerializer, UserLoginSerializer

# Create your views here.


class RegisterAPIView(APIView):
    def post(self, request, format=None):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                response_serializer = UserRegisterSerializer(user)
                return Response({
                    "success": True,
                    "message": "User creation done",
                    "data": response_serializer.data
                }, status=status.HTTP_201_CREATED)

            # ⚠️ Must return this if serializer is not valid
            return Response(
                {
                    "success": False,
                    "message": "Validation failed",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except IntegrityError as e:
            return Response(
                {
                    "success": False,
                    "message": "Integrity error",
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "An unexpected error occurred",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
