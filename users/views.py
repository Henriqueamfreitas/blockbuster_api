from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import UserSerializer


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()
        serializer = UserSerializer(new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
