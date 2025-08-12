Simple currency converter that works by using OpenAI's function calling functionality.
The user inputs the desired conversion query (e.g. "How many American Dollars am I getting for 100 Euros?", and the models extracts all the neccesary features.
For conversion, the model calls a public exchange rates API.

The server is built with Python using FastAPI.

To run from the terminal use:

hypercorn main:app
