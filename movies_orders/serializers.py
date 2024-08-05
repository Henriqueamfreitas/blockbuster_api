from rest_framework import serializers
from .models import MovieOrder


class MovieOrderSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    purchased_at = serializers.DateTimeField(read_only=True)
    purchased_by = serializers.CharField(read_only=True)

    def create(self, validated_data: dict):
        return MovieOrder.objects.create(**validated_data)