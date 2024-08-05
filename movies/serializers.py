from rest_framework import serializers
from .models import RatingMovie, Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    added_by = serializers.EmailField(source="user.email", read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(
        max_length=10, default="", required=False, allow_blank=True
    )
    rating = serializers.ChoiceField(choices=RatingMovie.choices, default=RatingMovie.G)
    synopsis = serializers.CharField(default="", required=False, allow_blank=True)

    def create(self, validated_data: dict):
        return Movie.objects.create(**validated_data)
