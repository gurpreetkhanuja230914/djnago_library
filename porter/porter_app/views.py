from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import MyUser,vehicle,categories,Order,Transaction
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import UserSignupSerializer,VehicleSerializer,categorySerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.renderers import JSONRenderer
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth import authenticate, login
from .forms import UserSignupForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import random
from django.contrib import messages



def index(request):
    return render(request, "porter_app/index.html")

class SignUpView(APIView):
    def get(self, request):
        form = UserSignupForm()
        return render(request, 'porter_app/signup.html', {'form': form})

    def post(self,request):
        serializer=UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token,created= Token.objects.get_or_create(user=user)
            
            return redirect('login')
        return Response(serializer.errors,status=400)


class LoginView(APIView):
    def get(self, request):
        return render(request, 'porter_app/login.html')
    def post(self,request):
        email=request.data.get("email")
        password=request.data.get("password")
        user = authenticate(request, username=email, password=password)
        print("user",user)
        
        if user:
            # Log the user in using Django's session-based authentication
            login(request, user)

            # Create or get the token for the user
            token, created = Token.objects.get_or_create(user=user)

            # Check the user type and redirect accordingly
            if user.user_type == "2":  # Driver
                # If the driver doesn't have a vehicle, redirect to add vehicle page
                if not vehicle.objects.filter(driver=user).exists():
                    c=categories.objects.all()
                    response = redirect('add_vehicle')
                    response['Authorization'] = f'Token {token.key}'
                    print(token)
                    return response
                return redirect('driver_dashboard')
            else:  # Client
                # Redirecting to 'booking' for clients
                response = redirect('booking')

                # Add the token to the response headers
                response['Authorization'] = f'Token {token.key}'
                
                return response

        # If authentication fails
        return JsonResponse({"error": "Invalid credentials"}, status=401)

class Add_vehicle_view(View):
    
    def post(self,request):
        print(request.user.user_type)

        category_id = request.POST.get('category')
        vehicle_model = request.POST.get('vehicle_model')
        vehicle_registration_number = request.POST.get('vehicle_registration_number')
        vehicle_state = request.POST.get('vehicle_state')
        print("vm",vehicle_model)
        # data = json.loads(request.body)

        # print(data.get('vehicle_model'))

        # vm=data.get('vehicle_model')
        # vehicle_registration_number=data.get('vehicle_registration_number')
        # vehicle_state=data.get('vehicle_state')
        if request.user.user_type=="1":
            serializer=VehicleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg":"vehicle has been added"})
            return Response({"error","only admin can add vehicle"})
        elif request.user.user_type=="2":
            print(category_id)
            category = categories.objects.get(category_id=category_id)
            v = vehicle.objects.create(
                vehicle_registration_number=vehicle_registration_number,
                vehicle_model=vehicle_model,
                vehicle_state=vehicle_state,
                category_id=category,
                driver_id=request.user.user_id
            )

            return redirect('driver_dashboard')
        return Response({"error":"unauthorized"},status=403)
    @method_decorator(login_required)
    def get(self,request):
        print(request.user)
        if request.user.user_type=="1":
            v=vehicle.objects.all()
        elif request.user.user_type=="2":
            v=vehicle.objects.filter(driver=request.user)
        else:
            return Response({"error","unauthorised"})
        cate=categories.objects.all()
        print(cate)

        return render(request, 'porter_app/add_vehicle.html', { 'categories': cate})
    
        
class add_category(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if request.user.user_type!="1":
            return Response({"error","only admin can add vehicle category"})
        serializer=categorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg","added category"})
        return Response(serializer.errors,status=401)
    def get(self,request):
        if request.user.user_type!="1":
            return Response({'error','admin have rights '})
        cs=categories.objects.all()
        serializer=categorySerializer(cs,many=True)
        json_data=JSONRenderer().render(serializer.data)
        return HttpResponse(json_data,content_type='application/json')
# @method_decorator(login_required, name='dispatch')   
class Booking(View):

    @method_decorator(login_required)
    def get(self, request):
        if request.user.user_type != "3":
            return redirect('index')  # Only clients allowed
        vehicles = vehicle.objects.all()
        context = {
        'categories': categories.objects.all()
        }
        return render(request, 'porter_app/booking.html',context)
    
    def post(self,request):
        print(request)
        # data = json.loads(request.body)
        
        pickup =request.POST.get('pickup_location')
        print(pickup)
        drop=request.POST.get('drop_location')
        distance,time=get_distance(pickup,drop)
        print(time)
        if distance is None:
            
             return render(request, 'porter_app/booking.html', {
            'categories': categories.objects.all(),
            'error': 'Could not calculate distance. Please try again.'
        })
        vehicle_id=request.POST.get('vehicle_id')
        print(vehicle_id)
        v=vehicle.objects.filter(vehicle_id=vehicle_id).first()
        if not v:
            return render(request, 'porter_app/booking.html', {
            'categories': categories.objects.all(),
            'error': 'Selected vehicle not found.'
        })
        print(v)
        ppk=v.category_id.per_km_price
        user=request.POST.get('user_id')
        print("distance is ",distance)
        payment_method=request.POST.get('payment_method')
        user = request.user
        amount=distance * ppk
        amount=round(amount,2)
        order=Order.objects.create(
            user_id=user,
            vehicle_id=v,
            pickup_location=pickup,
            drop_location=drop,
            amount=amount,
            payment_method=payment_method

        )
        # return render(request, 'porter_app/booking_confirm.html', {
        #     'vehicles': vehicle.objects.all(),
        #     'success': 'Booking successful!',
        #     "amount":amount,
        #     "distance":distance,
        #     "time":time,
        #     "order":order,
        # })
        return redirect('booking_confirm',order_id=order.id,distance=distance,amount=amount,time=time)
    
def get_vehicles(request, category_id):
    vehicles = vehicle.objects.filter(category_id=category_id)
    data = {
        "vehicles": [
            {"vehicle_id": v.vehicle_id, "name": v.vehicle_registration_number, "model": v.vehicle_model}
            for v in vehicles
        ]
    }
    return JsonResponse(data)
def booking_confirm(request,order_id,distance,amount,time):
    order_id = int(order_id)
    distance = float(distance)
    amount = float(amount)
    time = float(time)
    o=Order.objects.get(id=order_id)
    print(o.status)
    otp =random.randint(1111,9999)
    print("bookinh_confirm")
    o.abc=otp
    o.save()
    # return redirect('booking_confirm',order_id=order_id,distance=distance,amount=amount,time=time)

    return render(request, 'porter_app/booking_confirm.html',{'order_id':order_id,'distance':distance,'amount':amount,'time':time,'status':o.status,"otp":otp})





import requests
ORS_API_KEY = '5b3ce3597851110001cf6248de8d600977364a80aa273f986b70928b'
def get_coordinates(location_name):
    print(f"Getting coordinates for: {location_name}")

    url = "https://api.openrouteservice.org/geocode/search"
    params = {
        "api_key": ORS_API_KEY,
        "text": location_name,
        "size": 1
    }

    res = requests.get(url, params=params)
    print("Geocoding Response Status Code:", res.status_code)
    data = res.json()
    print("Geocoding Response Data:", data)

    if 'features' not in data or not data['features']:
        raise ValueError(f"No coordinates found for: {location_name}")

    coords = data['features'][0]['geometry']['coordinates']  # [lng, lat]
    print(f"Coordinates for '{location_name}': {coords}")
    return coords

def get_distance(pickup_name, drop_name):
    try:
        print("Calculating distance between:")
        print("Pickup:", pickup_name)
        print("Drop:", drop_name)

        start_coords = get_coordinates(pickup_name)
        end_coords = get_coordinates(drop_name)

        print("Start Coords:", start_coords)
        print("End Coords:", end_coords)

        route_url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {
            'Authorization': ORS_API_KEY,
            'Content-Type': 'application/json'
        }
        body = {
            "coordinates": [start_coords, end_coords]
        }

        print("Sending routing request with body:", body)
        res = requests.post(route_url, json=body, headers=headers)
        print("Routing Response Status Code:", res.status_code)
        route_data = res.json()
        print("Routing Response Data:", route_data)

        if 'routes' not in route_data or not route_data['routes']:
            raise ValueError("No route found in response")

        distance_meters = route_data['routes'][0]['segments'][0]['distance']
        duration_seconds = route_data['routes'][0]['segments'][0]['duration']

        # distance_meters = route_data['features'][0]['properties']['segments'][0]['distance']
        distance_km = distance_meters / 1000.0
        duration_minutes = duration_seconds / 60.0
        distance_km=round(distance_km, 2)
        duration_minutes=round(duration_minutes,2)
        print(f"Distance: {distance_km} km")
        return distance_km,duration_minutes

    except Exception as e:
        print("❌ Error fetching distance:", e)
        return None
@method_decorator(login_required, name='dispatch')
class DriverDashboardView(View):
    def get(self, request):
        if request.user.user_type != '2':  # Only allow driver to see
            return redirect('porter_app/index.html')  # Or show 403 or error page

        # Retrieve orders related to the logged-in driver
        available_orders = Order.objects.filter(status='pending', driver__isnull=True)
        active_order = Order.objects.filter(driver=request.user.user_id, status='accepted').first()
        print(available_orders)     
        print(active_order)
        return render(request, 'porter_app/driver_booking.html', {
            'available_orders': available_orders,
            'active_order': active_order,
        })
        

    def post(self, request):
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')

        # Get the order that the driver is interacting with
        order = get_object_or_404(Order, id=order_id, driver=request.user)

        if action == 'accept':
            # Ensure the driver hasn't already accepted another order
            if Order.objects.filter(driver=request.user, status='accepted').exists():
                return render(request, 'porter_app/driver_booking.html', {
                    'orders': Order.objects.filter(status="pending"),
                    'error': 'You can only accept one order at a time.'
                })
            order.driver=request.user
            order.status = 'accepted'
        
        elif action == 'reject':
            order.status = 'rejected'

        order.save()

        return redirect('driver_dashboard')
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    print("user_email",order.user_id)
    print(request.user)

    user=MyUser.objects.get(email=order.user_id)
    driver=MyUser.objects.get(email=request.user)
    order.driver_id=driver.user_id
    order.save()
    if request.method == 'POST':
        action = request.POST.get('action')
        otp=request.POST.get('otp')
        print("otp",otp)
        print(order.status)
        print(order.drop_location)
        print(order.payment_method)
        print(order.abc,"djdhjd")
        if order.abc==otp:
            if action == 'pickup' and order.status == 'pending':
                
                order.status = 'accepted'
                print(order.id)
                order.driver_id=driver.user_id
                print("order_driver_id",order.driver_id)
                Transaction.objects.create(order_id_id=order_id,status="on the way")
                # transaction = Transaction.objects.filter(order_id_id=order.id).first()
                # transaction.status='on the way'
                # transaction.save()
                order.save()
                send_mail(
                    subject='Your Order Has Been Picked Up!',
                    message='Hi there, your order has been picked up and is on the way!',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[order.user_id,],
                    fail_silently=False,
                )

            elif action == 'delivered' and order.status == 'accepted':
                transaction = Transaction.objects.filter(order_id_id=order_id).first()
                if transaction:
                    transaction.status = 'delivered'
                    transaction.save()
                send_mail(
                    subject='Your Order Has Been Delivered!',
                    message='Hi there, your order has been Delivered next time order soon!',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[order.user_id,],
                    fail_silently=False,
                )
                return redirect('driver_dashboard')
        else:
            messages.error(request,"wrong otp try again")

        return redirect('order_detail', order_id=order.id)

    return render(request, 'porter_app/order_detail.html', {'order': order,"user":user})

def reject_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=order_id)
        order.status = 'rejected'
        order.save()
        return redirect('driver_dashboard') 
def all_booking(request):
    user=MyUser.objects.get(email=request.user)
    print(user.user_id)
    print(user,"user")
    bookings=Order.objects.filter(user_id_id=user.user_id)
    print(request.user)

    return render(request,'porter_app/booking.html',{"bookings":bookings})