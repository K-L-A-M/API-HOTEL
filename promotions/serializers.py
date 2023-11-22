from rest_framework import serializers
from .models import Promotion, PromotionType


class PromotionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    promotion_type = serializers.ChoiceField(choices=PromotionType.choices, default=PromotionType.NoPromotion)

    class Meta:
        model = Promotion
        fields = ['id', 'name', 'promotion_type', 'start_date', 'end_date', 'discount_percentage']
        extra_kwargs = {
            'name': {'required': False},
            "discount_percentage": {'required': False},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['promotion_type'] = PromotionType(instance['promotion_type']).label
        return representation
