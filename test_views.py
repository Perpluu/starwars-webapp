import httpx
import requests
from fastapi.testclient import TestClient
from unittest.mock import patch

from views import app


client = TestClient(app)


def test_read_number_of_planets():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Number of Planets": 61}


@patch("views.requests.get")
def test_get_movie_data(mock_get):
    mock_movie_data = {
        "title": "A New Hope",
        "characters": [
            "https://swapi.py4e.com/api/people/1/",
            "https://swapi.py4e.com/api/people/2/",
            "https://swapi.py4e.com/api/people/3/",
            "https://swapi.py4e.com/api/people/4/",
            "https://swapi.py4e.com/api/people/5/",
        ],
    }
    mock_character_data = [
        {"name": "Mark Hamill"},
        {"name": "Harrison Ford"},
        {"name": "Carrie Fisher"},
        {"name": "Peter Cushing"},
        {"name": "Alec Guinness"},
    ]
    mock_get.side_effect = [
        type(
            "MockResponse",
            (object,),
            {"status_code": 200, "json": lambda: mock_movie_data},
        ),
        type(
            "MockResponse",
            (object,),
            {"status_code": 200, "json": lambda: mock_character_data[0]},
        ),
        type(
            "MockResponse",
            (object,),
            {"status_code": 200, "json": lambda: mock_character_data[1]},
        ),
        type(
            "MockResponse",
            (object,),
            {"status_code": 200, "json": lambda: mock_character_data[2]},
        ),
        type(
            "MockResponse",
            (object,),
            {"status_code": 200, "json": lambda: mock_character_data[3]},
        ),
        type(
            "MockResponse",
            (object,),
            {"status_code": 200, "json": lambda: mock_character_data[4]},
        ),
    ]

    # Test positive scenario
    response = client.post("/movie", {"movie_id": 1})
    assert response.status_code == 200
    assert response.json() == {
        "movie_name": "A New Hope",
        "actors": [
            "Mark Hamill",
            "Harrison Ford",
            "Carrie Fisher",
            "Peter Cushing",
            "Alec Guinness",
        ],
    }

    # Test movie not found
    response = client.post("/movie", {"movie_id": 999})
    assert response.status_code == 200
    assert response.json() == {"error": "Movie with ID 999 not found."}

    # Test invalid input
    response = app.post("/movie", {"movie_id": "not_an_integer"})
    assert response.status_code == 422
