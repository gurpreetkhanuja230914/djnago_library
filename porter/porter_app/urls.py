from django.urls import path
from . import views

urlpatterns=[
    path("",views.index),
    path("login/",views.LoginView.as_view(),name="login"),
    path("signup/",views.SignUpView.as_view(),name="signup"),
    path("vehicle/",views.Add_vehicle_view.as_view(),name="add_vehicle"),
    path("vehicle/category",views.add_category.as_view()),
    path("user/booking/",views.Booking.as_view(),name="booking"),
    path("user/booking/confirm/<str:order_id>/<str:distance>/<str:amount>/<str:time>/",views.booking_confirm,name="booking_confirm"),
    path("user/booking/all_booking",views.all_booking,name='all_booking'),
    path('get-vehicles/<int:category_id>/', views.get_vehicles, name='get_vehicles'),
    path('driver/dashboard/',views.DriverDashboardView.as_view(), name='driver_dashboard'),
    path('driver/dashboard/order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('driver/dashboard/order/<int:order_id>/reject/', views.reject_order, name='reject_order'),
]

