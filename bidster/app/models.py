from django.db import models


class OfferCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()


class ImageGalery(models.Model):
    pass

class Image(models.Model):
    galery_id = models.ForeignKey(ImageGalery, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Media/Public')
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
    image_gallery = models.OneToOneField(ImageGalery, on_delete=models.CASCADE)
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

    def __str__(self):
        return f'${self.pk} ${self.name}'


class Bid(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    message = models.CharField(max_length=200)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
