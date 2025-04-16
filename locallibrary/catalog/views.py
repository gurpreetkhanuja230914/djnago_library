from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from django.db import transaction
from .models import Employee
from .serializers import Employeeserializer,NameSerializer
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import io 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
# Create your views here.
from .models import CreateModelm,CreateProductLog
# def index(request):
#     s={"nonu":"moti","poonam":"motii"}
#     return JsonResponse(s)
# class based view in djnago drf 
# class APIsview(APIView):
#     def get(self,requests,format=None):
#         colors=["orange","red","yellow"]
#         return Response({
#             'msg':"cheerful colors","colors":colors
#         })
#     def post(self,requests):
#         serailizer=NameSerializer(data=requests.data)
#         if serailizer.is_valid():
#             name=serailizer.data.get('name')
#             msg="hello dear {}".format(name)
#             return Response({'msg':msg})
#         return Response(serailizer.errors,status=400)
    


#class viewset 
class Viewsets(viewsets.ViewSet):
    def list(self,requests):
        colors=["pink","green","purple","black"]
        return Response({"msg":"beautiful colors are","colors":colors})
    def create(self,requests):
        serializer=NameSerializer(data=requests.data)
        if serializer.is_valid():
            name=serializer.data.get('name')
            msg="Hello beautiful {}".format(name)
            return Response({"msg":msg})
        return Response(serializer.errors,status=400)
    def update(self,requests,pk=None):
        return Response({'msg':"you are in update"})
    def destroy(self,requests,pk=None):
        return Response({"msg":"you are in destroy"})
    def partial_update(self,requests,pk=None):
        return Response({"msg":"you are in partial updatee brooo"})
    





# method to check json response
class Jsoncbv(View):
    def get(self,requests,*args,**kwargs):
        s={"nonu":"acchhi","poonam":"bahot acchii"}
        return JsonResponse(s)
    
# class based view for get method 
@method_decorator(csrf_exempt,name='dispatch')
class EmployeeCBV(View):
    def get(self,requests,*args,**kwargs):
        json_data=requests.body
        print(json_data)
        json_data=list(json_data)
        print(json_data)
        # request with header body
        if json_data :
            json_data=requests.body
            stream=io.BytesIO(json_data)

            print("stream",stream)
            jss=JSONParser().parse(stream)
            name=jss.get('emp_name',None)
            emp=Employee.objects.get(emp_name=name)
            serializer=Employeeserializer(emp)
            json_data=JSONRenderer().render(serializer.data)
            return HttpResponse(json_data,content_type='application/json')
        # without any body content request
        qs=Employee.objects.all()
        serializer=Employeeserializer(qs,many=True)
        json_data=JSONRenderer().render(serializer.data)
        return HttpResponse(json_data,content_type='application/json')
    
    # post method of class based view
    def post(self,requests,*args,**kwargs):
        json_data=requests.body
        stream=io.BytesIO(json_data)
        js=JSONParser().parse(stream)
        serializer=Employeeserializer(data=js)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            msg={"msg":"data inserted successfully"}
            json_data=JSONRenderer().render(msg)
            return HttpResponse(json_data,content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type='application/json')
    
    # put method to update in sereailizer
    def put(self,requests,*args,**kwargs):
        json_data=requests.body
        stream=io.BytesIO(json_data)
        js=JSONParser().parse(stream)
        emp_no=js.get('id')
        emp=Employee.objects.get(id=emp_no)
        # emp is data in database which is saved previously for that particular emp no
        # data is which we want to change 
        serializer=Employeeserializer(emp,data=js,partial=True)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            msg={"msg":"updated successfully"}
            msg=JSONRenderer().render(msg)
            return HttpResponse(msg,content_type='application/json')
        se=JSONRenderer().render(serializer.errors)
        return HttpResponse(se,content_type='application/json')
    
   
    
            
        
    
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


        