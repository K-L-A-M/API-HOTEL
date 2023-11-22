from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'room', 'check_in_date', 'check_out_date', 'is_paid', 'transaction']
