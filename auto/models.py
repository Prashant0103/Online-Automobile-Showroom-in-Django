from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class category(models.Model):
    type_of_vehicle = models.CharField(max_length=250, default='Coupe')
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type_of_vehicle


class company(models.Model):
    cname = models.CharField(max_length=200, default='BMW')
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cname


engpower = [tuple([i, i]) for i in range(1, 11)]


class car(models.Model):
    name = models.CharField(max_length=100, blank=False)
    cmp = models.ForeignKey(company, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(category, on_delete=models.CASCADE, default=1)
    engine = models.IntegerField(choices=engpower)
    seat_capacity = models.IntegerField(choices=engpower)
    price = models.IntegerField(blank=False)
    image = models.ImageField(upload_to='images', blank=False)
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class cart(models.Model):
    car_name = models.ForeignKey(car, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    added_on = models.DateTimeField(auto_now_add=True, null=True)
    update_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    cust_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_ids = models.CharField(max_length=250)
    product_ids = models.CharField(max_length=250)
    invoice_id = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    processed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cust_id.username


class contact(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    msg = models.TextField(max_length=150, blank=False)

    def __str__(self) -> str:
        return self.name

