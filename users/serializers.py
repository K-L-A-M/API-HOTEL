from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from rooms.models import Room
from users.models import TypeUser


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(validators=[
        UniqueValidator(
            queryset=User.objects.all(),
            message="A user with this email already exists.",
        )
    ])
    password = serializers.CharField(write_only=True)
    contact = serializers.CharField(max_length=15)
    cpf = serializers.CharField(max_length=14, validators=[
        UniqueValidator(
            queryset=User.objects.all(),
            message="A user with this cpf already exists.",
        )
    ])
    nationality = serializers.CharField(max_length=50, required=False,)
    emergency_contact = serializers.CharField(max_length=15, required=False, allow_blank=True)
    favorite_rooms = serializers.PrimaryKeyRelatedField(many=True, queryset=Room.objects.all(), required=False)
    type_user = serializers.ChoiceField(choices=TypeUser.choices)

    def create(self, validated_data: dict) -> User:
        type_user = validated_data.get("type_user", TypeUser.USER)

        if type_user == TypeUser.ADMIN:
            return User.objects.create_superuser(**validated_data)
        else:
            return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "name",
            "contact",
            "cpf",
            "nationality",
            "emergency_contact",
            "favorite_rooms",
            "type_user",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "favorite_rooms": {"read_only": True}
        }
