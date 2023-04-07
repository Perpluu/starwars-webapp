import httpx
import requests
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, call
import pytest

from views import app, get_movie_data


client = TestClient(app)


def test_read_number_of_planets():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Number of Planets": 61}


@pytest.mark.asyncio
async def test_get_movie_data():
    with patch("requests.get") as mock_get:
        movie_data = {
            "title": "A New Hope",
            "characters": [
                "https://swapi.py4e.com/api/people/1/",
                "https://swapi.py4e.com/api/people/2/",
            ],
        }
        character_data = [{"name": "Luke Skywalker"}, {"name": "C-3PO"}]

        # Set up the mock responses
        mock_responses = [
            Mock(status_code=200, json=lambda: movie_data),
            Mock(status_code=200, json=lambda: character_data[0]),
            Mock(status_code=200, json=lambda: character_data[1]),
        ]
        mock_get.side_effect = mock_responses

        result = await get_movie_data(1)

        # Assert that the mock was called correctly
        mock_get.assert_has_calls(
            [
                call("https://swapi.py4e.com/api/films/1/"),
                call().json(),
                call(movie_data["characters"][0]),
                call().json(),
                call(movie_data["characters"][1]),
                call().json(),
            ]
        )
