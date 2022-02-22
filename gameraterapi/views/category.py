from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.db.models import Count, Q
from gameraterapi.models import Category

class CategoryView(ViewSet):

    def list(self, request):
        categories=Category.objects.all()
        
        serializer=CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        try:
            category=Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'label')
        depth = 1
