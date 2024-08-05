from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated
from .permissions import IsProfileOwner


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()
        serializer = UserSerializer(new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get(self, request: Request, user_id) -> Response:
        user = User.objects.filter(id=user_id)
        self.check_object_permissions(request, user[0])
        serializer = UserSerializer(user[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, user_id) -> Response:
        user = User.objects.filter(id=user_id)
        self.check_object_permissions(request, user[0])
        serializer = UserSerializer(user[0], request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        serializer = UserSerializer(updated_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
