from rest_framework import serializers
from . models import Book

class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields='__all__'
#First approach
# class BookSerializers(serializers.Serializer):
#     image=serializers.URLField(max_length=200, allow_blank=True)
#     book_title=serializers.CharField(max_length=100)
#     author=serializers.CharField(max_length=100)
#     details = serializers.CharField()

#     #deSerializers
#     def create(self,validated_data):
#         return Book.objects.create(**validated_data)
#     def update(self,instance,validated_data):
#         instance.image=validated_data.get('image',instance.image)
#         instance.book_title=validated_data.get('book_title',instance.book_title)
#         instance.author=validated_data.get('author',instance.author)
        
#         instance.save()
#         return instance