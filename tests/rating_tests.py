from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gameraterapi.models import GameRating, Game, Category

class GameRatingTests(APITestCase):
    def setUp(self):
        """create a new Player and collect the auth Token
        """
        # Define the URL path for registering a Player
        url = '/register'

        # Define the Player properties
        player = {
            "username": "steve",
            "password": "Admin8*",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        # Initiate POST request and capture the response
        response = self.client.post(url, player, format='json')

        # Store the TOKEN from the response data
        self.token = Token.objects.get(pk=response.data['token'])

        # Use the TOKEN to authenticate the requests
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # SEED THE DATABASE WITH A CATEGORY and a GAME
        # This is necessary because the API does not
        # expose a /games or /categories URL paths for creating Games and Categories

        # Create a new instance of Category
        category = Category()
        category.title = "Board Game"


        # Save the category to the testing database
        category.save()


        # Create a new instance of Game
        game = Game()
        game.title = "Clue"
        game.description = "More fun than a Barrel Of Monkeys!"
        game.designer = "Milton Bradley"
        game.year_released = 1920
        game.number_of_players = 6
        game.est_playtime = 5
        game.age_recommendation = 3
        game.player_id = self.token.user_id

        # Save the game to the testing database
        game.save()
        game.categories.set([1])


    def test_create_game_rating(self):
        """Ensure we can create (POST) a new game_rating
        """

        # Define the URL path for creating a new game_rating
        url = "/ratings"

        # Define the Game_rating properties
        game_rating = {
            "gameId": 1,
            "rating": 4
        }

        # Initiate the POST request and capture the response
        response = self.client.post(url, game_rating, format='json')

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the values are correct
        self.assertEqual(response.data['game']['id'], game_rating['gameId'])
        self.assertEqual(response.data['player']['id'], self.token.user_id)
        self.assertEqual(response.data['rating'], game_rating['rating'])


    # def test_get_game_rating(self):
    #     """ Ensure we can GET an existing game_rating"""

    #     # Create a new instance of a game_rating
    #     game_rating = GameRating()
    #     game_rating.label = "Board Game"

    #     # Save te game_rating to the testing database
    #     game_rating.save()

    #     # Define the url path for getting a single game_rating
    #     url = f'/ratings/{game_rating.id}'

    #     # Initiate GET request and capture the response
    #     response = self.client.get(url)

    #     # Assert that the response status code is 204 (NO CONTENT)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Assert that the values are correct
    #     self.assertEqual(response.data['label'], game_rating.label)


    def test_change_game_rating(self):
        """ Ensure we can change an existing game_rating"""

        # Create a new instance of a game_rating
        game_rating = GameRating()
        game_rating.game_id = 1
        game_rating.rating = 4
        game_rating.player_id = self.token.user_id

        # Save te game_rating to the testing database
        game_rating.save()

        # Define the url path for updating an existing game_rating
        url = f'/ratings/{game_rating.id}'

        # Define NEW game_rating properties
        new_game_rating = {
            "gameId": 1,
            "rating": 7
        }

        # Initiate PUT request and capture the response
        response = self.client.put(url, new_game_rating, format="json")

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture that response
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data['game']['id'], new_game_rating['gameId'])
        self.assertEqual(response.data['rating'], new_game_rating['rating'])
        self.assertEqual(response.data['player']['id'], self.token.user_id)


    # def test_delete_game_rating(self):
    #     """ Ensure we can delete an existing game_rating
    #     """

    #     # Create a new instance of a game_rating
    #     game_rating = GameRating()
    #     game_rating.label = "Board Game"

    #     # Sve the game_rating to the testing database
    #     game_rating.save()

    #     # define the URL path for deleting an existing game_rating
    #     url = f'/ratings/{game_rating.id}'

    #     # Initiate the DELETE request and capture the response
    #     response = self.client.delete(url)

    #     # Assert that the response status code is 204 (NO CONTENT)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #     # Initiate GET request and capture the response
    #     response = self.client.get(url)

    #     # Assert that the response status code is 404 (NOT FOUND)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
