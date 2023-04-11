import requests
from fastapi import FastAPI
import httpx
import asyncio

app = FastAPI()

@app.get("/")
async def read_number_of_planets():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://swapi.py4e.com/api/planets/")
        planets = response.json()
        return {"Number of Planets": planets["count"]}


@app.post("/movie/{movie_id}")
async def get_movie_data(movie_id: int):
    async with httpx.AsyncClient() as movie:
        response = await movie.get(f"https://swapi.py4e.com/api/films/{movie_id}/")
        movie_data = response.json()
        movie_name = movie_data["title"]
        actor_urls = movie_data["characters"]
        tasks = [movie.get(actor_url) for actor_url in actor_urls]
        actors_response = await asyncio.gather(*tasks)
        actor_names = [actor["name"] for actor in [r.json() for r in actors_response]]
        return {"movie_name": movie_name, "actors": actor_names}
