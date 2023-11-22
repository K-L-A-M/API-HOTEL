from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    user = serializers.UUIDField(format='hex', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_cpf = serializers.CharField(source='user.cpf', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'user',
            'user_name',
            'user_cpf',
            'method',
            'timestamp',
            'amount_paid',
            'discount_percentage',
            'discount_amount',
        ]
        read_only_fields = ['id', 'timestamp', 'discount_percentage', 'discount_amount']

    def calculate_discounts(self, room, check_in_date, check_out_date):
        discount_percentage = 0
        discount_amount = 0

        if room.promotions.exists():
            promotion = room.promotions.first()

            if promotion.promotion_type in ['discount in daily', 'extended stay discount']:
                discount_percentage = promotion.discount_percentage

            elif promotion.promotion_type == 'discount':
                discount_amount = promotion.discount_amount

        return discount_percentage, discount_amount

    def calculate_amount_paid(self, data):
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')
        room = data.get('room')

        if check_in_date and check_out_date and room:
            discount_percentage, discount_amount = self.calculate_discounts(room, check_in_date, check_out_date)
            price_per_night = room.price_per_night
            delta_days = (check_out_date - check_in_date).days
            total_amount = delta_days * price_per_night
            amount_paid = total_amount - discount_amount
            amount_paid = max(amount_paid, 0)

            return amount_paid, discount_percentage, discount_amount

        return 0, 0, 0

    def create(self, validated_data):
        user = validated_data.pop('user')
        user_id = user.id
        amount_paid, discount_percentage, discount_amount = self.calculate_amount_paid(validated_data)

        transaction = Transaction.objects.create(user_id=user_id, amount_paid=amount_paid, **validated_data)

        user_name = user.name if user.name else "N/A"

        response_data = {
            'id': transaction.id,
            'user': {
                'id': user_id,
                'name': user_name,
                'cpf': user.cpf,
            },
            'amount_paid': amount_paid,
            'timestamp': transaction.timestamp,
            'discount_percentage': discount_percentage,
            'discount_amount': discount_amount,
            'method': transaction.method,
        }

        return response_data
