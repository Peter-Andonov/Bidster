from os.path import join

from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth.models import User


class OfferCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to=join(
        settings.MEDIA_ROOT, 'categories'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Offer categories"


class ImageGalery(models.Model):

    class Meta:
        verbose_name_plural = "Image galeries"


class Image(models.Model):
    galery = models.ForeignKey(ImageGalery, on_delete=models.CASCADE)
    image = models.ImageField()
    default = models.BooleanField(default=False)


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
    current_price = models.DecimalField(max_digits=19, decimal_places=2)
    category = models.ForeignKey(
        OfferCategory, null=True, on_delete=models.SET_NULL)
    image_galery = models.OneToOneField(ImageGalery, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    published_on = models.DateTimeField(default=now, editable=False)
    is_active = models.BooleanField(default=True, editable=False)
    expires_on = models.DateTimeField(editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=50)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50)
    view_counts = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.name


class Bid(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    message = models.CharField(max_length=200)
    for_offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=now, editable=False)
