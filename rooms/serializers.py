from rest_framework import serializers
from .models import Room, RoomFeature, Bed
from promotions.serializers import PromotionSerializer


class RoomFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomFeature
        fields = ['name']


class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = ['bed_type', 'quantity', 'room']


class RoomSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    promotions = PromotionSerializer(many=True, read_only=True)
    beds = BedSerializer(many=True, read_only=True)
    features = RoomFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'floor', 'room_number', 'capacity', 'is_occupied', 'price_per_night', 'promotions', 'beds', 'features']
        extra_kwargs = {
            'id': {'read_only': True},
            'promotions': {'read_only': True},
            'beds': {'read_only': True},
            'features': {'read_only': True},
        }
