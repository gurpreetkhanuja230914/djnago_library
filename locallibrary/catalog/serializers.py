from rest_framework import serializers
class Employeeserializer(serializers.Serializer):
    emp_name=serializers.CharField(max_length=30)
    emp_salary=serializers.IntegerField()
    emp_no=serializers.IntegerField()
    emp_address=serializers.CharField(max_length=100)