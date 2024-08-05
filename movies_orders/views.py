from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import MovieOrderSerializer
from rest_framework.permissions import IsAuthenticated
from movies.models import Movie


class MovieOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int) -> Response:
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie = Movie.objects.filter(id=movie_id)[0]
        validated_data = serializer.validated_data
        validated_data["user"] = request.user
        validated_data["movie"] = movie
        new_data = serializer.save()
        serializer = MovieOrderSerializer(new_data).data
        serializer["purchased_by"] = request.user.email
        serializer["title"] = movie.title

        return Response(serializer, status=status.HTTP_201_CREATED)
