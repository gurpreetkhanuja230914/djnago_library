from django.db import models


# class CheapProductManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(price__lt=50)
    
# Create your models here.
class CreateModelm(models.Model):
    name=models.CharField(max_length=30)
    price=models.IntegerField()
    dates=models.DateField(auto_now_add=True)
    # cheap_objects = CheapProductManager()
class CreateProductLog(models.Model):
    product=models.ForeignKey(CreateModelm,on_delete=models.CASCADE)
    action=models.CharField(max_length=100)
    created_at=models.DateField(auto_now_add=True)