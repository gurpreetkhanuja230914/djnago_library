from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.


class categories(models.Model):
    category_id=models.AutoField(primary_key=True)
    category_name=models.CharField(max_length=30)
    category_size=models.CharField(max_length=30)
    category_holds_upto=models.IntegerField()
    per_km_price=models.FloatField()
    def __str__(self):
        return self.category_name


class vehicle(models.Model):
    vehicle_id=models.AutoField(primary_key=True)
    vehicle_model=models.CharField(max_length=30)
    vehicle_registration_number=models.CharField(max_length=30)
    vehicle_state=models.CharField(max_length=30)
    category_id=models.ForeignKey(categories,on_delete=models.CASCADE)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)


class Usermanager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('the email must be set')
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    def super_user(self,email,password=None,**extra_fields):
        extra_fields.setdefault('user_type','admin')
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email,password,**extra_fields)
    
    
class MyUser(AbstractBaseUser,PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    user_types=((1,'Admin'),(2,'Driver'),(3,'client'))
    name=models.CharField(max_length=30,null=True)
    adhar_no=models.CharField(max_length=16,null=True,blank=True)
    address=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    user_type=models.CharField(default=3,choices=user_types,max_length=10)
    bank_account_number = models.CharField(max_length=30, null=True, blank=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']
    objects=Usermanager()

    def __str__(self):
        return self.email
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    driver = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        null=True,
        limit_choices_to={'user_type': 2},
        related_name='driver_orders'  # Add a unique related_name
    )
    
    user_id = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='user_orders'  # Add a unique related_name
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    order_time = models.DateTimeField(auto_now_add=True)
    vehicle_id = models.ForeignKey(vehicle, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=100)
    drop_location = models.CharField(max_length=100)
    amount = models.FloatField(default=0)
    payment_method = models.CharField(max_length=30)
    abc=models.CharField(max_length=20)
    
    def __str__(self):
        return f"Order by {self.user_id.email} for {self.driver.email if self.driver else 'No driver'}"
class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pickup', 'Pickup'),
        ('on the way', 'On the way'),
        ('delivered', 'Delivered'),
    )
    transaction_id=models.AutoField(primary_key=True)
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pickup')
