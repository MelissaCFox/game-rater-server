from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gameraterapi.models import Category

class CategoryTests(APITestCase):
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


    # def test_create_category(self):
    #     """Ensure we can create (POST) a new category
    #     """

    #     # Define the URL path for creating a new category
    #     url = "/categories"

    #     # Define the Category properties
    #     category = {
    #         "label": "Board Game"
    #     }

    #     # Initiate the POST request and capture the response
    #     response = self.client.post(url, category, format='json')

    #     # Assert that the response status code is 201 (CREATED)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     # Assert that the values are correct
    #     self.assertEqual(response.data['label'], category['label'])


    def test_get_category(self):
        """ Ensure we can GET an existing category"""

        # Create a new instance of a category
        category = Category()
        category.label = "Board Game"

        # Save te category to the testing database
        category.save()

        # Define the url path for getting a single category
        url = f'/categories/{category.id}'

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data['label'], category.label)


    # def test_change_category(self):
    #     """ Ensure we can change an existing category"""

    #     # Create a new instance of a category
    #     category = Category()
    #     category.label = "Board Game"

    #     # Save te category to the testing database
    #     category.save()

    #     # Define the url path for updating an existing category
    #     url = f'/categories/{category.id}'

    #     # Define NEW category properties
    #     new_category = {
    #         "label": "RPG"
    #     }

    #     # Initiate PUT request and capture the response
    #     response = self.client.put(url, new_category, format="json")

    #     # Assert that the response status code is 204 (NO CONTENT)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #     # Initiate GET request and capture that response
    #     response = self.client.get(url)

    #     # Assert that the response status code is 200 (OK)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Assert that the values are correct
    #     self.assertEqual(response.data['label'], new_category['label'])


    # def test_delete_category(self):
    #     """ Ensure we can delete an existing category
    #     """

    #     # Create a new instance of a category
    #     category = Category()
    #     category.label = "Board Game"

    #     # Sve the category to the testing database
    #     category.save()

    #     # define the URL path for deleting an existing category
    #     url = f'/categories/{category.id}'

    #     # Initiate the DELETE request and capture the response
    #     response = self.client.delete(url)

    #     # Assert that the response status code is 204 (NO CONTENT)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #     # Initiate GET request and capture the response
    #     response = self.client.get(url)

    #     # Assert that the response status code is 404 (NOT FOUND)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
