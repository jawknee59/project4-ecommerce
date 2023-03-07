from django.db import models

# A tuple of 2-tuples
CATEGORIES = (
    ("E", "Electronics"),
    ("J", "Jewelery"),
    ("MC", "Men's Clothing"),
    ("WC", "Women's Clothing")
)

# Create your models here.
# Item Model
class Item(models.Model):
    title = models.TextField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(max_length=250)
    category = models.CharField(
        max_length=2,
        choices = CATEGORIES,
        default = CATEGORIES[0][0]
    )

    def __str__(self):
        return self.title

class Cart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()