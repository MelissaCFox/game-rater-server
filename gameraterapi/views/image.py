import base64
import uuid
from django.core.files.base import ContentFile

from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from gameraterapi.models import Game, Player, GameImage


class GameImageView(ViewSet):

    def list(self, request):
        images=GameImage.objects.all()
        
        serializer=GameImageSerializer(images, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            game_image=GameImage.objects.get(pk=pk)
            serializer = GameImageSerializer(game_image)
            return Response(serializer.data)
        except GameImage.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        game = Game.objects.get(pk=request.data['gameId'])
        player = Player.objects.get(user=request.auth.user)

        format, imgstr = request.data["image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), 
                           name=f'{request.data["gameId"]}-{uuid.uuid4()}.{ext}')

        image = GameImage.objects.create(
            game = game,
            player = player,
            image = data
        )
        
        serializer = GameImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GameImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameImage
        fields = ('id', 'game', 'player', 'image')
        depth = 1
