from django.db import models
from django.utils import timezone as tz
from django.contrib.auth.models import User

class Customer(models.Model):
    login_account = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    female = models.BooleanField()                                 
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=225, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    # is_biker = models.BooleanField(default=True)
    # last_longitude = models.DecimalField(default=0, max_digits=9, decimal_places=6, null=True, blank=True) 
    # last_latitude = models.DecimalField(default=0, max_digits=9, decimal_places=6, null=True, blank=True)
    
    created_date = models.DateTimeField(default=tz.now)
    
    def __str__(self):
        return self.first_name
    
    def display_date_of_birth(self):
        return self.date_of_birth.strftime("%m/%d/%Y")
    
    def display_created_date(self):
        return self.created_date.strftime("%m/%d/%Y")
    
    def display_fullname(self):
        return f'{self.last_name} {self.first_name}'