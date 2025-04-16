from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class categories(models.Model):
    category_id=models.CharField(30)
    category_name=models.CharField(30)
    def __str__(self):
        return self.category_name


class vehicle(models.Model):
    vehicle_id=models.CharField(25)
    vehicle_model=models.CharField(30)
    vehicle_name=models.CharField(30)
    vehicle_state=models.CharField(30)
    category_id=models.ForeignKey(categories,on_delete=models.CASCADE)

class MyUser(AbstractUser):
    user_types=((1,'Admin'),(2,'Driver'),(3,'user'))
    user_type=models.CharField(default=1,choices=user_types,max_length=10)

class Admin(models.Model):
    admin=models.OneToOneField(MyUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Driver(models.Model):
    name=models.CharField(max_length=30)
    experience=models.FloatField()
    adhar_no=models.CharField(max_length=16)
    address=models.CharField(max_length=100)
    admin=models.OneToOneField(MyUser,on_delete=models.CASCADE)


class user(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    mobile_no=models.CharField(max_length=10)
    admin=models.OneToOneField(MyUser,on_delete=models.CASCADE)

@receiver(post_save,sender=MyUser)
def user_created(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Admin.objects.create(admin=instance)
        if instance.user_type==2:
            Driver.objects.create(admin=instance)
        if instance.user_type==3:
            user.objects.create(admin=instance)
# @receiver(post_save,sender=MyUser)
# def user_save(sender,instance,created,**kwargs):
#     if instance.user_type==1:
#         instance.Admin.save()
#     if instance.user_type==2:
#         instance.Driver.save()
#     if instance.user_type==3:
#         instance.user.save()
    


    

# class User()