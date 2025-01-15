from django.db.models.signals import post_save
from .models import TelegramUser, Transaction
from django.dispatch import receiver
from decimal import Decimal


@receiver(post_save, sender=Transaction)
def handle_transaction_completed(sender, instance, created, **kwargs):
    if instance.transaction_type == "deposit" and instance.status == "completed":
        user = instance.user
        amount = instance.amount

        amount_float = float(amount)

        user.balance = user.balance + amount_float
        user.save()

    elif instance.transaction == "withdrawal" and instance.status == "completed":
        user = instance.user
        amount = instance.amount
        amount_float = float(amount)

        if user.profit >= amount:
            user.profit = user.profit - amount_float
            user.save()



