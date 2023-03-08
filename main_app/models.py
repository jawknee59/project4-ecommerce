from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=1000)
    category = models.CharField(
        max_length=2,
        choices = CATEGORIES,
        default = CATEGORIES[0][0]
    )
    image_url = models.CharField(max_length=200)

    def __str__(self):
        return self.title

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user

    def get_total_price(self):
        total_price = 0
        for item in self.cartitem_set.all():
            total_price += item.total_price()
        return total_price

# Item(s) in cart Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.cart.user, self.item, self. quantity

    # function to get qty * price of one item 
    def total_price(self):
        return self.quantity * self.price


      


