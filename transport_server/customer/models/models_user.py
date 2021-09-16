from django.db import models
from django.utils import timezone as tz

class User(models.Model):
    phone_number = models.CharField(max_length=15, primary_key=True)
    email = models.TextField(null=True, blank=True)
    password = models.TextField()
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