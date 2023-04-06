# starwars-webapp

README

Description

This is a simple Python code that uses FastAPI and httpx libraries to fetch the number of planets from the Star Wars API (SWAPI).

The code defines an endpoint / that returns the number of planets available in the SWAPI. It uses the httpx library to make an HTTP GET request to the SWAPI, and then returns the count of planets in the response as a JSON object.

Installation

To run this code, you will need Python 3.6 or higher installed on your system. You can install the required libraries using pip, by running the following command:

pip install -r requirements.txt

To run the code, save it as a Python file (e.g. main.py) and execute the following command in your terminal:

uvicorn main:app --reload

This will start a local server at http://127.0.0.1:8000/. You can open this URL in your web browser to access the endpoint. 

Return after running the app: 

{"Number of Planets": 60}
