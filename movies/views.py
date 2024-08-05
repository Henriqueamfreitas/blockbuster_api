from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import MovieSerializer
from .permissions import IsAdminOrReadOnly
from .models import Movie


class MovieView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data["user"] = request.user
        new_movie = serializer.save()
        serializer = MovieSerializer(new_movie).data
        serializer["added_by"] = request.user.email

        return Response(serializer, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieDetailView(APIView):
    def get(self, request: Request, movie_id: int) -> Response:
        movie = Movie.objects.filter(id=movie_id)
        serializer = MovieSerializer(movie[0])

        return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = Movie.objects.filter(id=movie_id)
        movie[0].delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
