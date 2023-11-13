from django.db import models
from uuid import uuid4
from transactions.models import Transaction
from users.models import User
from rooms.models import Room


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    transaction = models.OneToOneField(Transaction, null=True, blank=True, on_delete=models.SET_NULL)
