from datetime import datetime
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models import Count, Q
from gameraterapi.models import GameRating, Game, Player

class GameRatingView(ViewSet):

    def list(self, request):
        game_ratings=GameRating.objects.all()
  
        serializer=GameRatingSerializer(game_ratings, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            game_rating=GameRating.objects.get(pk=pk)
            serializer = GameRatingSerializer(game_rating)
            return Response(serializer.data)
        except GameRating.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        game = Game.objects.get(pk=request.data["gameId"])
        player = Player.objects.get(user=request.auth.user)
        game_rating=GameRating.objects.create(
            game = game,
            player = player,
            rating = request.data['rating']
        )
        
        try:
            game_rating.save()
            serializer = GameRatingSerializer(game_rating)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        game_rating = GameRating.objects.get(pk=pk)
        game_rating.rating = request.data['rating']
        game = Game.objects.get(pk=request.data["gameId"])
        game_rating.game = game
        
        try:
            game_rating.save()
            serializer = GameRatingSerializer(game_rating)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk):
        game_rating = GameRating.objects.get(pk=pk)
        game_rating.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GameRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameRating
        fields = ('id', 'game', 'player', 'rating')
        depth = 1
