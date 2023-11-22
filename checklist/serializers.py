from rest_framework import serializers
from reserves.models import Reservation
from .models import CheckList


class CheckListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    user = serializers.UUIDField(format='hex')
    room = serializers.UUIDField(format='hex')
    is_reserved = serializers.BooleanField(default=False)
    check_in_date = serializers.DateTimeField(required=False)
    check_out_date = serializers.DateTimeField(required=False)

    class Meta:
        model = CheckList
        fields = [
            'id',
            'user',
            'room',
            'check_in_date',
            'check_out_date',
            'is_reserved',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        is_reserved = validated_data.get('is_reserved', False)

        if is_reserved:
            reservation = Reservation.objects.create(
                user_id=validated_data['user'],
                room_id=validated_data['room'],
                check_in_date=validated_data.get('check_in_date'),
                check_out_date=validated_data.get('check_out_date'),
                is_paid=True
            )

            validated_data['check_in_date'] = reservation.check_in_date
            validated_data['check_out_date'] = reservation.check_out_date

        return super().create(validated_data)
