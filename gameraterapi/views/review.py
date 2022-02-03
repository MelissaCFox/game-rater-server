from datetime import datetime
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models import Count, Q
from gameraterapi.models import GameReview, Game, Player

class GameReviewView(ViewSet):

    def list(self, request):
        reviews=GameReview.objects.all()
  
        serializer=ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            review=GameReview.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except GameReview.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        game = Game.objects.get(pk=request.data["gameId"])
        player = Player.objects.get(user=request.auth.user)
        review=GameReview.objects.create(
            game = game,
            player = player,
            review = request.data['review'],
            date_time = datetime.now()
        )
        
        try:
            review.save()
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        review = GameReview.objects.get(pk=pk)
        review.review = request.data['review']
        game = Game.objects.get(pk=request.data["gameId"])
        review.game = game
        
        try:
            review.save()
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk):
        review = GameReview.objects.get(pk=pk)
        review.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameReview
        fields = ('id', 'game', 'player', 'review', "date_time")
        depth = 1
