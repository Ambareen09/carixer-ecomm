from django.db import models
from django.contrib import admin

from django.core.validators import MaxValueValidator, MinValueValidator

STATUS = {
    ("DELIVERED", "DELIVERED"),
    ("CANCELLED", "CANCELLED"),
    ("ORDERED", "ORDERED"),
}


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
    # featured = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class Review(BaseModel):
    rate = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rate)


class OrderDetail(BaseModel):
    status = models.CharField(choices=STATUS, max_length=255, null=True)
    date = models.DateField(null=True)
    order_id = models.CharField(max_length=255, null=True)
    size = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, related_name="orderedProduct")
    address = models.TextField(null=True)
    short_description = models.TextField(null=True)
    long_description = models.TextField(null=True)

    def __str__(self):
        return str(self.status) + " | " + str(self.order_id)


admin.site.register(Product)
admin.site.register(Review)
admin.site.register(OrderDetail)
