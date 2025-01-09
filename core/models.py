from django.db import models

# Create your models here.
class TelegramUser(models.Model):
    telegram_id = models.IntegerField()
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    balance = models.FloatField(default=0.0)
    referral_code = models.CharField(max_length=10)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} or {self.telegram_id}"

    def save(self, *args, **kwargs):
        if not self.referral_code:
            import random
            import string
            # Generate unique referral code
            while True:
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                if not TelegramUser.objects.filter(referral_code=code).exists():
                    self.referral_code = code
                    break
        super().save(*args, **kwargs)


class CryptoAddress(models.Model):
    CURRENCY_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('USDT_TRC20', 'USDT TRC20'),
        ('USDT_ERC20', 'USDT ERC20'),
        ('XRP', 'Ripple'),
        ('SOL', 'Solana'),
    ]

    NETWORK_CHOICES = [
        ('BITCOIN', 'Bitcoin'),
        ('TRC20', 'Tron TRC20'),
        ('ERC20', 'Ethereum ERC20'),
        ('XRP', 'Ripple'),
        ('SOLANA', 'Solana'),
    ]

    currency = models.CharField(max_length=20, choices=CURRENCY_CHOICES, unique=True)
    network = models.CharField(max_length=20, choices=NETWORK_CHOICES)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    memo = models.CharField(max_length=100, blank=True, null=True)  # For currencies that need memo/tag
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Crypto Address'
        verbose_name_plural = 'Crypto Addresses'

    def __str__(self):
        return f"{self.get_currency_display()} - {self.address[:10]}..."
