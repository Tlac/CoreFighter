from django.db import models

class GundamCard(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    rarity = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    level = models.IntegerField()
    cost = models.IntegerField()
    color = models.CharField(max_length=50)
    type = models.CharField(max_length=100)
    effect = models.TextField()
    zone = models.CharField(max_length=100)
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