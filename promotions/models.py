# models/promotion.py
from django.db import models
from uuid import uuid4


class PromotionType(models.TextChoices):
    NoPromotion = "No Promotion", "NP"
    BreakFast = "BreakFast", "BF"
    DiscountInDaily = "Discount in Daily", "DD"
    ExtendedStayDiscount = "Extended stay Discount", "ED"
    Discount = "discount", "D"


class Promotion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=256, blank=True, null=True)
    promotion_type = models.CharField(choices=PromotionType.choices, default=PromotionType.NoPromotion)
    start_date = models.DateField(null=False)
    end_date = models.DateField(blank=True)
    discount_percentage = models.PositiveIntegerField(null=True, blank=True)
