from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.db.models import Count, Q
from gameraterapi.models import Game
from gameraterapi.models.game_image import GameImage

class GameView(ViewSet):

    def list(self, request):
        games=Game.objects.all()
        
        serializer=GameSerializer(games, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            game=Game.objects.get(pk=pk)
            # images = GameImage.objects.get(game=game)
            # game.images = images

            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        game = Game.objects.create(
            title = request.data['title'],
            description = request.data['description'],
            designer = request.data['designer'],
            year_released = request.data['yearReleased'],
            number_of_players = request.data['numberOfPlayers'],
            est_playtime = request.data['estPlaytime'],
            age_recommendation = request.data['ageRecommendation']
        )
        game.categories.set(request.data['categories'])
        
        serializer = GameSerializer(game)
        return Response (serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, pk):
        try:
            game=Game.objects.get(pk=pk)
            game.title = request.data['title']
            game.description = request.data['description']
            game.designer = request.data['designer']
            game.year_released = request.data['yearReleased']
            game.number_of_players = request.data['numberOfPlayers']
            game.est_playtime = request.data['estPlaytime']
            game.age_recommendation = request.data['ageRecommendation']

            game.categories.set(request.data['categories'])

            game.save()
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'year_released', 'number_of_players',
                  'est_playtime', 'age_recommendation', 'categories', 'reviews', 'average_rating',
                  'images')
        depth = 3
