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
    
    created_date = models.DateTimeField(default=tz.now)
    
    def __str__(self):
        return self.first_name