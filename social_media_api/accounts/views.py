from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import RegisterSerializer, LoginSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomUser

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = Token.objects.get(user=user)

        return Response({
            "user": user.username,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token = serializer.validated_data["token"]

        return Response({
            "user": user.username,
            "token": token
        })


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "bio": request.user.bio,
        })

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):

    users = CustomUser.objects.all()

    user_to_follow = get_object_or_404(users, id=user_id)

    if user_to_follow == request.user:
        return Response({"error": "You cannot follow yourself"}, status=400)

    request.user.following.add(user_to_follow)

    return Response({"message": f"You are now following {user_to_follow.username}"})

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    users = CustomUser.objects.all()
    user_to_unfollow = get_object_or_404(users, id=user_id)

    request.user.following.remove(user_to_unfollow)

    return Response({"message": f"You unfollowed {user_to_unfollow.username}"})



