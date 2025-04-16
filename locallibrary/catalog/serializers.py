from rest_framework import serializers
from .models import Employee


# create modelserializer module 
class Employeeserializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields='__all__'
        #fieds=('emp_name','emp_salary')
        # exclude=('emp_name','emp_salary')
class NameSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=27)
    

# def multiples_of_1000(value):
#     print("-------------")
#     if value%1000 != 0:
#         raise serializers.ValidationError("salary should be multiple of 1000")
#     return value
# # using serailizer module 
# class Employeeserializer(serializers.Serializer):
#     emp_name=serializers.CharField(max_length=30)
#     emp_salary=serializers.IntegerField(validators=[multiples_of_1000,])
#     emp_no=serializers.IntegerField()
#     emp_address=serializers.CharField(max_length=100)

#     def create(self,validated_data):
#         return Employee.objects.create(**validated_data)
    
#     def update(self,instance,validated_data):
#         instance.emp_name=validated_data.get('emp_name',instance.emp_name)
#         instance.emp_salary=validated_data.get('emp_salary',instance.emp_salary)
#         instance.emp_no=validated_data.get('emp_no',instance.emp_no)
#         instance.emp_address=validated_data.get('emp_address',instance.emp_address)
#         instance.save()
#         return instance
    
#     #field level validation
#     def validate_emp_salary(self,value):
#         if value<2000:
#             raise serializers.ValidationError("employee salary should be greater than 2000")
#         return value
    
#     #object level validation
#     def validate(self,data):
#         ename=data.get('emp_name')
#         e_salary=data.get('emp_salary')
#         if ename.lower()=='purnima':
#             if e_salary <12000:
#                 raise serializers.ValidationError("purnima salary should be greater than 12000")
#         return data

# # validation using validator 

    