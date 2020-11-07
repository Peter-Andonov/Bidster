from django.db import models


class OfferCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()


class Offer(models.Model):

    UNKNOWN = 'X'
    NEW = 'N'
    USED = 'U'

    CONDITION_TYPE_CHOICES = (
        (UNKNOWN, 'Unknown'),
        (NEW, 'New'),
        (USED, 'Used'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    condition = models.CharField(
        max_length=1,
        choices=CONDITION_TYPE_CHOICES,
        default=UNKNOWN,
    )
    starting_price = models.DecimalField(max_digits=19, decimal_places=2)
    category = models.ForeignKey(OfferCategory, on_delete=models.DO_NOTHING)
    location = models.CharField(max_length=50)
    published_on = models.DateTimeField()
    expires_in = models.DateTimeField()
    view_counts = models.PositiveIntegerField()


class Bid(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    message = models.CharField(max_length=200)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
