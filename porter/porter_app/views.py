from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import MyUser,vehicle,categories,Order
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


def index():
    return HttpResponse("welcome to porter")

class SignUpView(APIView):
    def post(self,request):
        serializer=UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token,created= Token.objects.get_or_create(user=user)
            return Response({"msg":"user created successfully","token":token.key},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=400)


class LoginView(APIView):
    def post(self,request):
        email=request.data.get("email")
        password=request.data.get("password")
        user=authenticate(request,email=email,password=password)
        if user:
            token,created=Token.objects.get_or_create(user=user)
            return Response({"msg":"login successful","token":token.key})
        return Response({"error","invalid credential"},status=401)

class Add_vehicle_view(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        print(request.user.user_type)
        if request.user.user_type!="1":
            return Response({"error","only admin can add vehicle"})
        serializer=VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg","vehicle has been added"})
        return Response(serializer.errors,status=400)
    def get(self,request):
        if request.user.user_type!="1":
            return Response({"error","only admin have rights vehicle"})
        v=vehicle.objects.all()
        serializer=VehicleSerializer(v,many=True)
        json_data=JSONRenderer().render(serializer.data)
        return HttpResponse(json_data,content_type='application/json')
    
        
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
    def post(self,request):
        print(request)
        data = json.loads(request.body)
        
        pickup =data.get('pickup_location')
        print(pickup)
        drop=data.get('drop_location')
        distance=get_distance(pickup,drop)
        vehicle_id=data.get('vehicle_id')
        print(vehicle_id)
        v=vehicle.objects.filter(vehicle_id=vehicle_id).first()
        print(v)
        ppk=v.category_id.per_km_price
        user=data.get('user_id')
        payment_method=data.get('payment_method')
        user = MyUser.objects.get(user_id=user)
        amount=distance * ppk
        Order.objects.create(
            user_id=user,
            vehicle_id=v,
            pickup_location=pickup,
            drop_location=drop,
            amount=amount,
            payment_method=payment_method

        )
        return HttpResponse("booking created successfully")
    





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


        # distance_meters = route_data['features'][0]['properties']['segments'][0]['distance']
        distance_km = distance_meters / 1000.0
        print(f"Distance: {distance_km} km")
        return distance_km

    except Exception as e:
        print("❌ Error fetching distance:", e)
        return None
