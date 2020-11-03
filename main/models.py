from django.db import models
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)

    def get_category_url(self):
        return reverse("main:index_by_category", kwargs={
            'category_id': self.id
        })

    def __str__(self):
        return self.title

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to="image")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:product", kwargs={
            'pk': self.id

        })
    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart", kwargs={
            'pk': self.id
        })

    def get_remove_from_cart_url(self):
        return reverse("main:remove-from-cart", kwargs={
            'pk': self.id
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.TextField(blank=True, null=True)
    bank_account = models.IntegerField(blank=True, null=True)
    receiver_name = models.CharField(max_length=20, blank=True, null=True)
    delivered= models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total