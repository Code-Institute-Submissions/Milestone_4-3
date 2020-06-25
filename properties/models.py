from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Feature(models.Model):
    name = models.CharField(max_length=254)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Image(models.Model):
    property = models.ForeignKey('Property', null=False, blank=False, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1024, null=False, blank=False)
    image_name = models.ImageField(null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.image

class Property(models.Model):
    # TODO add here agent
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    short_description = models.CharField(max_length=254)
    address = models.CharField(max_length=254)
    postcode = models.CharField(max_length=8)
    long_description = models.TextField()
    monthly_price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image_name = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.short_description
