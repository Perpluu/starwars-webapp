from fastapi import FastAPI
import aiohttp

app = FastAPI()

@app.get("/")
async def get_planets():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://swapi.py4e.com/api/planets/") as response:
            data = await response.json()
    return {"Number of planets": data["count"]}
