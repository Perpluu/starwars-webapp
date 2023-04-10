import httpx
import requests
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient

from views import app


client = TestClient(app)


def test_get_movie_data():
    # Mock the requests.get function
    requests.get = MagicMock(
        return_value=MockResponse(
            {
                "title": "A New Hope",
                "characters": ["https://swapi.py4e.com/api/people/1/"],
            }
        )
    )

    # Mock the response from the people API
    requests.get().json = MagicMock(return_value={"name": "Luke Skywalker"})

    # Make the request to the endpoint
    response = client.post("/movie/1")

    # Check the response
    assert response.status_code == 200
    assert response.json() == {"movie_name": "A New Hope", "actors": ["Luke Skywalker"]}


def test_read_number_of_planets():
    # Mock the httpx.AsyncClient.get function
    httpx.AsyncClient.get = AsyncMock(return_value=MockResponse({"count": 61}))

    # Make the request to the endpoint
    response = client.get("/")

    # Check the response
    assert response.status_code == 200
    assert response.json() == {"Number of Planets": 61}


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data
