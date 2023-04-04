from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/")
async def read_number_of_planets():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://swapi.py4e.com/api/planets/")
        planets = response.json()
        return {"Number of Planets": planets["count"]}
