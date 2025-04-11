from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
# Create your views here.
from .models import CreateModelm,CreateProductLog
def index(request):
    return HttpResponse("you are at home")
def search_view(request):
    q=request.GET.get("q")
    q="apple"
    CreateModelm.objects.filter(name__icontains=q)
    return render()
@transaction.atomic
def create_product(request):
    try:
        product=CreateModelm.objects.create(name="Test",price=50)
        CreateProductLog.objects.create(product=product,action="Created Product")
        return HttpResponse("Product and logs are successfully generated ")
    except Exception as e:
        return HttpResponse(f"error {e}")
    
@transaction.atomic
def successful_transaction(request):
    product=CreateModelm.objects.create(name="apple",price=20)
    CreateProductLog.objects.create(product=product,action="product created")
    def after_commit():
        print("email send to admin after commit")
    transaction.on_commit(after_commit)
    return HttpResponse("Success product and logs saved")
@transaction.atomic
def fail_transaction(request):
    product=CreateModelm.objects.create(name="Tablet",price=20)
    raise Exception("simulated failure after product creation")
    CreateProductLog.objects.create(product=product,action="product created")
    return HttpResponse("this wont be reached ")
def nested_transaction(request):
    try :
        with transaction.atomic():
            product=CreateModelm.objects.create(name="nasaaa",price=20)
            try:
                with transaction.atomic():
                    CreateProductLog.objects.create(product=None,action="invalid string")
            except:
                print("inner error caught")
            CreateProductLog.objects.create(product=product,action="valid log")
        return HttpResponse("outer commited inner fail ")
    except Exception as e:
        return HttpResponse(f" failes {e}")
def manual_rollback(request):
    with transaction.atomic():
        product=CreateModelm.objects.create(name="namas",price=153)
        if product.price >150 :
            transaction.set_rollback(True)
            return HttpResponse("product has been rollback manually")
        CreateProductLog.objects.create(product=product,action="rollback")
        return HttpResponse("product and log saved")


        