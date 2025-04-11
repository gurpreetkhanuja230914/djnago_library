from django.urls import path,include
# from .views import index,create_product
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("create/",views.create_product,name="create_product"),
     path("success/",views.successful_transaction),
    path("fail/", views.fail_transaction),
    path("nested/", views.nested_transaction),
    path("rollback/", views.manual_rollback),
]