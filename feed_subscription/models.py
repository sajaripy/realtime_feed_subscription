from django.db import models

# Create your models here.
class UserSubscription(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    feed_name = models.CharField(max_length=100)  # e.g., "Binance Trades"
    subscribed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.feed_name}"