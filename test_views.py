import httpx
import requests
from fastapi.testclient import TestClient
from unittest.mock import patch
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
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "title": "A New Hope",
            "characters": [
                "https://swapi.py4e.com/api/people/1/",
                "https://swapi.py4e.com/api/people/2/",
            ],
        }

        result = await get_movie_data(1)

        mock_get.assert_called_once_with("https://swapi.py4e.com/api/films/1/")
        assert result == {
            "movie_name": "A New Hope",
            "actors": ["Luke Skywalker", "C-3PO"],
        }
