from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gameraterapi.models import Game, Category

class GameTests(APITestCase):
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
        
       # SEED THE DATABASE WITH A CATEGORY
        # This is necessary because the API does not
        # expose a /categories URL path for creating Categorys

        # Create a new instance of Category
        category = Category()
        category.label = "Board game"

        # Save the Category to the testing database
        category.save()


    def test_create_game(self):
        """Ensure we can create (POST) a new game
        """

        # Define the URL path for creating a new game
        url = "/games"

        # Define the Game properties
        game = {
            "title": "Clue",
            "description": "More fun than a Barrel Of Monkeys!",
            "designer": "Milton Bradley",
            "yearReleased": 1920,
            "numberOfPlayers": 6,
            "estPlaytime": 5,
            "ageRecommendation": 5,
            "categories": [1]
        }

        # Initiate the POST request and capture the response
        response = self.client.post(url, game, format='json')

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the values are correct
        self.assertEqual(response.data['title'], game['title'])
        self.assertEqual(response.data['description'], game['description'])
        self.assertEqual(response.data['designer'], game['designer'])
        self.assertEqual(response.data['year_released'], game['yearReleased'])
        self.assertEqual(response.data['number_of_players'], game['numberOfPlayers'])
        self.assertEqual(response.data['est_playtime'], game['estPlaytime'])
        self.assertEqual(response.data['age_recommendation'], game['ageRecommendation'])
        self.assertEqual(response.data['player']['user']['id'], self.token.user_id)
        self.assertIsNotNone(response.data['categories'])

        
    def test_get_game(self):
        """ Ensure we can GET an existing game"""

        # Create a new instance of a game
        game = Game()
        game.title = "Clue"
        game.description = "More fun than a Barrel Of Monkeys!"
        game.designer = "Milton Bradley"
        game.year_released = 1920
        game.number_of_players = 6
        game.est_playtime = 5
        game.age_recommendation = 3
        game.player_id = self.token.user_id

        # Save te game to the testing database
        game.save()
        game.categories.set([1])

        # Define the url path for getting a single game
        url = f'/games/{game.id}'

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data['title'], game.title)
        self.assertEqual(response.data['description'], game.description)
        self.assertEqual(response.data['designer'], game.designer)
        self.assertEqual(response.data['year_released'], game.year_released)
        self.assertEqual(response.data['number_of_players'], game.number_of_players)
        self.assertEqual(response.data['est_playtime'], game.est_playtime)
        self.assertEqual(response.data['age_recommendation'], game.age_recommendation)
        self.assertEqual(response.data['player']['user']['id'], self.token.user_id)
        self.assertIsNotNone(response.data['categories'])


    def test_change_game(self):
        """ Ensure we can change an existing game"""

        # Create a new instance of a game
        game = Game()
        game.title = "Clue"
        game.description = "More fun than a Barrel Of Monkeys!"
        game.designer = "Milton Bradley"
        game.year_released = 1920
        game.number_of_players = 6
        game.est_playtime = 5
        game.age_recommendation = 3
        game.player_id = self.token.user_id

        # Save te game to the testing database
        game.save()
        game.categories.set([1])

        # Define the url path for updating an existing game
        url = f'/games/{game.id}'

        # Define NEW game properties
        new_game = {
            "title": "Clue 2",
            "description": "So much more fun than a Barrel Of Monkeys!",
            "designer": "Milton Bradley Co",
            "yearReleased": 1925,
            "numberOfPlayers": 5,
            "estPlaytime": 4,
            "ageRecommendation": 3,
            "categories": [1]
        }

        # Initiate PUT request and capture the response
        response = self.client.put(url, new_game, format="json")

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture that response
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data['title'], new_game['title'])
        self.assertEqual(response.data['description'], new_game['description'])
        self.assertEqual(response.data['designer'], new_game['designer'])
        self.assertEqual(response.data['year_released'], new_game['yearReleased'])
        self.assertEqual(response.data['number_of_players'], new_game['numberOfPlayers'])
        self.assertEqual(response.data['est_playtime'], new_game['estPlaytime'])
        self.assertEqual(response.data['age_recommendation'], new_game['ageRecommendation'])
        self.assertEqual(response.data['player']['user']['id'], self.token.user_id)
        self.assertIsNotNone(response.data['categories'])


    def test_delete_game(self):
        """ Ensure we can delete an existing game
        """
        # Create a new instance of a game
        game = Game()
        game.title = "Clue"
        game.description = "More fun than a Barrel Of Monkeys!"
        game.designer = "Milton Bradley"
        game.year_released = 1920
        game.number_of_players = 6
        game.est_playtime = 5
        game.age_recommendation = 3
        game.player_id = self.token.user_id

        # Save te game to the testing database
        game.save()
        game.categories.set([1])

        # define the URL path for deleting an existing game
        url = f'/games/{game.id}'

        # Initiate the DELETE request and capture the response
        response = self.client.delete(url)

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 404 (NOT FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_get_all_games(self):
        """
        Ensure we can GET all games
        """
        # Create a new instance of a game
        game = Game()
        game.title = "Clue"
        game.description = "More fun than a Barrel Of Monkeys!"
        game.designer = "Milton Bradley"
        game.year_released = 1920
        game.number_of_players = 6
        game.est_playtime = 5
        game.age_recommendation = 3
        game.player_id = self.token.user_id

        # Save te game to the testing database
        game.save()
        game.categories.set([1])
        
        url = '/games'
        # Initiate GET request and capture the response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1 )
