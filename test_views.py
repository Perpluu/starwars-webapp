import httpx
from unittest.mock import Mock
from fastapi.testclient import TestClient

from views import app


client = TestClient(app)



def test_get_movie_data(httpx_mock):
    movie_id = 1
    movie_title = "A New Hope"
    httpx_mock.add_response(
        method="GET",
        url=f"https://swapi.py4e.com/api/films/{movie_id}/",
        json={"title": movie_title, "characters": ["https://example.com/yoda"]},
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=f"https://example.com/yoda",
        json={"name": "Luke Skywalker"},
        status_code=200,
    )

    response = client.post(f"/movie/{movie_id}")
    
    assert response.status_code == 200
    assert response.json() == {"movie_name": "A New Hope", "actors": ["Luke Skywalker"]}


# why context manager mock is so complicatetd:
# client = httpx.AsyncClient()
# await client.__aenter__()
# response = await client.get("https://swapi.py4e.com/api/planets/")
# planets = response.json()
# await client.__aexit__()

def test_read_number_of_planets(mocker):
    mock = mocker.patch("httpx.AsyncClient", spec=httpx.AsyncClient)
    response_mock = Mock(spec=httpx.Response)
    response_mock.json.return_value = {"count" : 61}
    mock.return_value.__aenter__.return_value.get.return_value = response_mock

    # Make the request to the endpoint
    response = client.get("/")

    # Check the response
    assert response.status_code == 200
    assert response.json() == {"Number of Planets": 61}
