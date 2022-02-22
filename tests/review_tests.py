from datetime import datetime
from django.utils import timezone as tz
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gameraterapi.models import GameReview, Game, Category

class GameReviewTests(APITestCase):
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


    def test_create_game_review(self):
        """Ensure we can create (POST) a new game_review
        """

        # Define the URL path for creating a new game_review
        url = "/reviews"

        # Define the Game_review properties
        game_review = {
            "gameId": 1,
            "review": "Great game",
        }

        # Initiate the POST request and capture the response
        response = self.client.post(url, game_review, format='json')

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the values are correct
        self.assertEqual(response.data['game']['id'], game_review['gameId'])
        self.assertEqual(response.data['player']['id'], self.token.user_id)
        self.assertEqual(response.data['review'], game_review['review'])
        
        ## !! Can't figure out how to compare date time when it should need to be passed in for post body
        ## !! and assertIsNotNone says date_time constraint fails NOT NONE
        ## !! comparing datetimes using assertAlmostEqual (stack overflow) not working either
        self.assertAlmostEqual(response.data['date_time'], datetime.now(), delta=tz.timedelta(seconds=1))


    # def test_get_game_review(self):
    #     """ Ensure we can GET an existing game_review"""

    #     # Create a new instance of a game_review
    #     game_review = GameReview()
    #     game_review.label = "Board Game"

    #     # Save te game_review to the testing database
    #     game_review.save()

    #     # Define the url path for getting a single game_review
    #     url = f'/reviews/{game_review.id}'

    #     # Initiate GET request and capture the response
    #     response = self.client.get(url)

    #     # Assert that the response status code is 204 (NO CONTENT)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Assert that the values are correct
    #     self.assertEqual(response.data['label'], game_review.label)


    def test_change_game_review(self):
        """ Ensure we can change an existing game_review"""

        # Create a new instance of a game_review
        game_review = GameReview()
        game_review.game_id = 1
        game_review.rating = 4
        game_review.player_id = self.token.user_id

        # Save te game_review to the testing database
        game_review.save()

        # Define the url path for updating an existing game_review
        url = f'/reviews/{game_review.id}'

        # Define NEW game_review properties
        new_game_review = {
            "gameId": 1,
            "rating": 7
        }

        # Initiate PUT request and capture the response
        response = self.client.put(url, new_game_review, format="json")

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture that response
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data['game']['id'], new_game_review['gameId'])
        self.assertEqual(response.data['rating'], new_game_review['rating'])
        self.assertEqual(response.data['player']['id'], self.token.user_id)


    # def test_delete_game_review(self):
    #     """ Ensure we can delete an existing game_review
    #     """

    #     # Create a new instance of a game_review
    #     game_review = GameReview()
    #     game_review.label = "Board Game"

    #     # Sve the game_review to the testing database
    #     game_review.save()

    #     # define the URL path for deleting an existing game_review
    #     url = f'/reviews/{game_review.id}'

    #     # Initiate the DELETE request and capture the response
    #     response = self.client.delete(url)

    #     # Assert that the response status code is 204 (NO CONTENT)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #     # Initiate GET request and capture the response
    #     response = self.client.get(url)

    #     # Assert that the response status code is 404 (NOT FOUND)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
