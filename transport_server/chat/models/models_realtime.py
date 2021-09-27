from django.db import models
from django.utils import timezone as tz
from django.contrib.auth.models import User

from customer.models import *

class CustomerReady(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    origin_lng = models.DecimalField(default=0, max_digits=9, decimal_places=6) 
    origin_lat = models.DecimalField(default=0, max_digits=9, decimal_places=6) 
    origin_address = models.TextField() 
    created_date = models.DateTimeField(default=tz.now)

    def __str__(self):
        return f'{self.customer.login_account.username} - {self.created_date.strftime("%m/%d/%Y, %H:%M:%S")}'

class DestinationInfo(models.Model):
    customer_ready = models.ForeignKey(CustomerReady, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    destination_lng = models.DecimalField(default=0, max_digits=9, decimal_places=6) 
    destination_lat = models.DecimalField(default=0, max_digits=9, decimal_places=6) 
    destination_address = models.TextField()
    weight = models.DecimalField(default=0, max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.phone} - {self.name}'

class DriverOnline(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    longitude = models.DecimalField(default=0, max_digits=9, decimal_places=6) 
    latitude = models.DecimalField(default=0, max_digits=9, decimal_places=6) 
    created_date = models.DateTimeField(default=tz.now)

    def __str__(self):
        return f'{self.customer.login_account.username} - {self.created_date.strftime("%m/%d/%Y, %H:%M:%S")}'
    
    def display_fullname(self):
        return f'{self.customer.last_name} {self.customer.first_name}'

class Shipment(models.Model):
    driver = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_ready = models.ForeignKey(CustomerReady, on_delete=models.CASCADE)
    price = models.IntegerField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.driver.first_name} - {self.customer_ready.customer.first_name}'
