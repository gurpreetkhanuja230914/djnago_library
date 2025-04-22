from django.urls import path
from . import views

urlpatterns=[
    path("",views.index),
    path("login/",views.LoginView.as_view(),name="login"),
    path("signup/",views.SignUpView.as_view(),name="signup"),
    path("vehicle/",views.Add_vehicle_view.as_view(),name='add_vehicle'),
    path("vehicle/category",views.add_category.as_view()),
    path("user/booking/",views.Booking.as_view(),name="booking"),
    path('get-vehicles/<int:category_id>/', views.get_vehicles, name='get_vehicles'),
    path('driver/dashboard/',views.DriverDashboardView.as_view(), name='driver_dashboard'),
]

