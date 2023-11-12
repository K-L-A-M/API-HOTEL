from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from uuid import uuid4
from users.models import User


class TransactionMethod(models.TextChoices):
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    CASH = "Cash"
    PIX = "Pix"


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_cpf = models.CharField(max_length=14, null=True, blank=True)
    user_name = models.CharField(max_length=150, null=True, blank=True)
    method = models.CharField(choices=TransactionMethod.choices, max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    discount_percentage = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.user_cpf = self.user.cpf
        self.user_name = self.user.name
        super().save(*args, **kwargs)
