import requests
from fastapi import FastAPI
import httpx

app = FastAPI()


@app.get("/")
async def read_number_of_planets():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://swapi.py4e.com/api/planets/")
        planets = response.json()
        return {"Number of Planets": planets["count"]}


@app.post("/movie/{movie_id}")
async def get_movie_data(movie_id: int):
    response = requests.get(f"https://swapi.py4e.com/api/films/{movie_id}/")
    movie_data = response.json()
    people = [
        requests.get(actor_url).json().get("name")
        for actor_url in movie_data.get("characters", [])
    ]
    movie_name = movie_data.get("title") if "title" in movie_data else None
    return {"movie_name": movie_name, "actors": people}
