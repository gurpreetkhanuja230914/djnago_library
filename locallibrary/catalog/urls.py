from django.urls import path,include
# from .views import index,create_product
from . import views
from rest_framework import routers
routers=routers.DefaultRouter()
routers.register('test_view',views.Viewsets,basename='test_view')

urlpatterns = [
    # path("",views.index,name="index"),
    path("",views.Jsoncbv.as_view()),
    path("api/",views.APIView.as_view()),
    path("emp/",views.EmployeeCBV.as_view()),
    path("create/",views.create_product,name="create_product"),
    path("success/",views.successful_transaction),
    path("fail/", views.fail_transaction),
    path("nested/", views.nested_transaction),
    path("rollback/", views.manual_rollback),
    path("",include(routers.urls)),
]