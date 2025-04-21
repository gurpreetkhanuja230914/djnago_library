from django.urls import path
from . import views

urlpatterns=[
    path("",views.index),
    path("login/",views.LoginView.as_view()),
    path("signup/",views.SignUpView.as_view()),
    path("admin/vehicle/",views.Add_vehicle_view.as_view()),
    path("admin/vehicle/category",views.add_category.as_view()),
    path("user/booking/",views.Booking.as_view()),
]

