from .models import Book
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializers
class CreateBook(APIView):
    def get(self,request,pk=None,format=None):
        id=pk;
        if id is not None:
            try:
                book=Book.objects.get(id=id)
                serializer=BookSerializers(book)
                return Response(serializer.data)
            except book.DoesNotExist:
                return Response('No data found', status=status.HTTP_404_NOT_FOUND)
        all_book=Book.objects.all()
        serializer=BookSerializers(all_book,many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer=BookSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Successfully save data')
        return Response(serializer.errors)
    def put(self,request,pk,format=None):
        id=pk
        book=Book.objects.get(id=id)
        serializer=BookSerializers(book,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Book update successfully')
        return Response(serializer.errors)
    def patch(self,request,pk,format=None):
        id=pk;
        book=Book.objects.get(id=id)
        serializer=BookSerializers(book,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Book patially update successfully')
        return Response(serializer.errors)   
    def delete(self,request,pk,format=None):
        id=pk
        book=Book.objects.get(id=id)
        book.delete()
        return Response('Book delete succssefully')         

# first_approach

# from django.shortcuts import render
# from .models import Book
# from .serializers import BookSerializers
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# import io
# # Create your views here.
# def book_info(request):
#     # complex_data
#     book=Book.objects.all()
#     #python dict
#     serializer=BookSerializers(book,many=True)
#     # jeson render
#     json_data=JSONRenderer().render(serializer.data)
#     return HttpResponse(json_data,content_type='application/json')

# def book_inst(request,pk):
#     book=Book.objects.get(id=pk)
#     serializer=BookSerializers(book)
#     json_data=JSONRenderer().render(serializer.data)
#     return HttpResponse(json_data,content_type='application/json')

# @csrf_exempt
# def create_book(request):
#     if request.method == "GET":
#         # Return a simple message or form (or a 405 response if you prefer)
#         res = {'Message': 'Use POST to create a new book.'}
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type='application/json')

#     elif request.method == "POST":
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythonData = JSONParser().parse(stream)
#         serializers = BookSerializers(data=pythonData)

#         if serializers.is_valid():
#             serializers.save()
#             res = {'Message': 'Book added successfully!'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json')
#         else:
#             json_data = JSONRenderer().render(serializers.errors)
#             return HttpResponse(json_data, content_type='application/json', status=400)

#     elif request.method == 'PUT':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythonData = JSONParser().parse(stream)
#         book_id = pythonData.get('id')

#         try:
#             book = Book.objects.get(id=book_id)
#         except Book.DoesNotExist:
#             res = {'Error': 'Book not found!'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json', status=404)

#         serializers = BookSerializers(book, data=pythonData, partial=True)
#         if serializers.is_valid():
#             serializers.save()
#             res = {'Message': 'Book updated successfully!'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json')
#         else:
#             json_data = JSONRenderer().render(serializers.errors)
#             return HttpResponse(json_data, content_type='application/json', status=400)

#     elif request.method == 'DELETE':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythonData = JSONParser().parse(stream)
#         book_id = pythonData.get('id')

#         try:
#             book = Book.objects.get(id=book_id)
#             book.delete()
#             res = {'Message': 'Book deleted successfully!'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json')
#         except Book.DoesNotExist:
#             res = {'Error': 'Book not found!'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json', status=404)

#     else:
#         res = {'Error': 'Invalid request method!'}
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type='application/json', status=405)





from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order
from sslcommerz_lib import SSLCOMMERZ
from django.shortcuts import redirect
# Create your views here.
import requests
class InitiatePayment(APIView):
    def post(self,request):
        print("Request Data:", request.data)
        amount=request.data.get('amount')
        
        if not amount:
            return Response({"error":"Amount is required"},status=status.HTTP_404_NOT_FOUND)
        if not request.user or not request.user.is_authenticated:
            return Response({"error": "User authentication required"}, status=status.HTTP_401_UNAUTHORIZED)        
        order= Order.objects.create(user=request.user, amount=amount)
        print(amount)
        print(request.user.id)
        settings = { 'store_id': 'testphitrkxd4', 'store_pass': 'phitr67c39cf9e26b5@ssl', 'issandbox': True }
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = amount
        post_body['currency'] = "BDT"
        post_body['tran_id'] = str(order.id)
        post_body['success_url'] = "http://127.0.0.1:8000/payment/success/"
        post_body['fail_url'] = "http://127.0.0.1:8000/payment/fail/"
        post_body['cancel_url'] = "http://127.0.0.1:8000/payment/cancel/"
        post_body['emi_option'] = 0
        post_body['cus_name'] = request.user.username
        post_body['cus_email'] = request.user.email
        post_body['cus_phone'] = request.user.phone
        post_body['cus_add1'] = "customer address"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        print(post_body)
        response=sslcz.createSession(post_body)
        return  redirect(response['GatewayPageURL']) 
        
class PaymentSuccess(APIView):
    def post(self, request):
        tran_id = request.data.get("tran_id")
        order = get_object_or_404(Order, id=tran_id)
        order.status = "SUCCESS"
        order.transaction_id = request.data.get("bank_tran_id")
        order.save()
        return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)


class PaymentFail(APIView):
    def post(self, request):
        tran_id = request.data.get("tran_id")
        order = get_object_or_404(Order, id=tran_id)
        order.status = "FAILED"
        order.save()
        return Response({"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)        



urlpatterns = [
    path('initiate/', InitiatePayment.as_view(), name='initiate_payment'),
    path('success/', PaymentSuccess.as_view(), name='payment_success'),
    path('fail/', PaymentFail.as_view(), name='payment_fail'),
]


from rest_framework import serializers
from .models import UserProfile,Order
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields='__all__'
        
class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, required= True)
    class Meta:
        model= UserProfile
        fields=['id','username','email','password']


from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserProfile(AbstractUser):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone=models.CharField(max_length=15)
    
    def __str__(self):
        return self.username
    
class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20, default='Pending')
    transaction_id=models.CharField(max_length=100,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Order {self.id} - {self.status}'
