from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    name = models.CharField(max_length = 64)
    description = models.CharField(max_length = 200, default="")
    price = models.DecimalField(max_digits = 9, decimal_places = 2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    buyer = models.ForeignKey(User, on_delete=models.SET_DEFAULT, related_name="winning", default=None, null=True)
    bids = models.IntegerField(default = 0)
    active = models.BooleanField(default = True)    

class Comment(models.Model):
    comment = models.CharField(max_length = 200)
    leaver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

class Watchlist(models.Model):
    watch_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watching")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched")