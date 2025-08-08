from rest_framework import serializers
from .models import Book, Author
import datetime


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        
    def validate(self, value):
        cuerrent_year = datetime.datetime.now().year
        if value > cuerrent_year:
            raise serializers.ValidationError('publication year can not be in the future')
        
class AuthorSerializer(serializers.ModelSerializer):
    
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']