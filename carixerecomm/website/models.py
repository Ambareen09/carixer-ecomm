from django.db import models
from django.contrib import admin

from django.core.validators import MaxValueValidator, MinValueValidator

class BaseModel(models.Model):
    objects = models.Manager
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.FileField()


class Review(BaseModel):
    rate = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


admin.site.register(Product)
admin.site.register(Review)
