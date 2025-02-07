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
