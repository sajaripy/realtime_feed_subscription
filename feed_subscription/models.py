from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=100)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('user', 'channel_id')