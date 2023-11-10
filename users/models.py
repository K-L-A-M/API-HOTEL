from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
import re
from django.core.exceptions import ValidationError
from rooms.models import Room


def validate_contact(value):
    regex = re.compile(
        r'^(?:(?:\+|00)?(\d{1,3}))?[-. (]*(\d{1,3})[-. )]*(\d{1,4})(?:[-. ]*(\d{1,4}))?(?:[-. ]*(\d{1,9}))?$'
    )
    if not regex.match(value):
        raise ValidationError(f"{value} is not a valid number")


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True, null=False)
    name = models.CharField(null=False, max_length=150)
    contact = models.CharField(max_length=15, null=False, validators=[validate_contact])
    cpf = models.CharField(max_length=14, null=False, unique=True)
    nationality = models.CharField(max_length=50)
    emergency_contact = models.CharField(max_length=15, blank=True)
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
    favorite_rooms = models.ManyToManyField(Room, related_name='favorited_by', blank=True)
