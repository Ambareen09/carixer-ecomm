from tkinter import CASCADE
from django.db import models
from django.contrib import admin
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator
STATUS = {
    ("DELIVERED", "DELIVERED"),
    ("CANCELLED", "CANCELLED"),
    ("ORDERED", "ORDERED"),
    ("INCART", "INCART"),
}

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class BaseModel(models.Model):
    objects = models.Manager
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    title = models.CharField(max_length=255)
    price = models.IntegerField(null=True)
    size = models.CharField(max_length=255)
    stock = models.IntegerField()
    image = models.FileField(upload_to="website/static/images")
    featured = models.BooleanField(default=False)
    short_description = models.TextField(null=True)
    long_description = models.TextField(null=True)
    status = models.CharField(max_length=255)

    def __str__(self):
        return str(self.title)


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rate)


class OrderDetail(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=255, null=True)
    date = models.DateField(null=True)
    order_id = models.CharField(max_length=255, null=True)
    quantity = models.IntegerField(null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, related_name="orderedProduct")
    country = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)
    apartment = models.CharField(max_length=255, null=True)
    postal_code = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)
    free_shipping = models.BooleanField(default=True)
    shipping_charge = models.FloatField(null=True, default=0)
    current_location = models.IntegerField(null=True)
    tracking_number = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    channel = models.CharField(max_length=255)

    def __str__(self):
        return str(self.status) + " | " + str(self.first_name)


class DeliveryCheckpoint(BaseModel):
    transit_index = models.IntegerField()
    order = models.ForeignKey(
        OrderDetail, on_delete=models.CASCADE, null=True, related_name="transitPoint")
    message = models.CharField(max_length=255)
    time = models.DateTimeField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return str(self.order) + " | " + str(self.transit_index)


class About(BaseModel):
    about_title = models.CharField(null=True, max_length=255)
    about = models.TextField(null=True)
    vision_title = models.CharField(null=True, max_length=255)
    vision = models.TextField(null=True)


class Waterless(BaseModel):
    waterless = models.TextField(null=True)


admin.site.register(Product)
admin.site.register(Review)
admin.site.register(OrderDetail)
admin.site.register(DeliveryCheckpoint)
admin.site.register(About)
admin.site.register(Waterless)
