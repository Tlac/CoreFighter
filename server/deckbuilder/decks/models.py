import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class GundamCard(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    rarity = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    level = models.IntegerField()
    cost = models.IntegerField()
    colour = models.CharField(max_length=50)
    type = models.CharField(max_length=100)
    effect = models.TextField()
    zone = models.JSONField(default=list)
    trait = models.JSONField()
    link = models.URLField(max_length=500)
    ap = models.CharField(max_length=50, null=True, blank=True)
    hp = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=200)
    set = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    original_image_url = models.URLField(max_length=500)

    def __str__(self):
        return self.name


class DeckList(models.Model):
    COLOUR_CHOICES = [
        ("green", "Green"),
        ("blue", "Blue"),
        ("red", "Red"),
        ("white", "White"),
        ("purple", "Purple"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    cards = models.JSONField()
    colours = models.JSONField()
    is_private = models.BooleanField(default=True)
    vote_count = models.IntegerField(default=0)

    def clean(self):
        # Validate that colours contains only 1 or 2 valid choices
        if not isinstance(self.colours, list):
            raise ValidationError("Colours must be a list.")
        if not (1 <= len(self.colours) <= 2):
            raise ValidationError("Your deck can only have one or two colours")
        for colour in self.colours:
            if colour not in dict(self.COLOUR_CHOICES):
                raise ValidationError(f"{colour} is not a valid colour.")

    def __str__(self):
        return self.name
