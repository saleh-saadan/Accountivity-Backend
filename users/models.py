import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


def generate_user_id():
    """
    Generates a random 5 character ID
    """
    # TODO: Find fix for possibly generating the same ID again, despite the low chances
   
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(5))


class User(AbstractUser):
    
    # Generate unique friend ID for each user
    user_id = models.CharField(
        max_length=5, default=generate_user_id, primary_key=True, editable=False
    )

    def __str__(self):
        return f"{self.username} ({self.user_id})"


class Friendships(models.Model):
    
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_friendships",
        on_delete=models.CASCADE,
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_friendships",
        on_delete=models.CASCADE,
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sender", "receiver")
        verbose_name_plural = "Friendships"

    def __str__(self):
        return f"{self.sender} --> {self.receiver} ({self.status})"
