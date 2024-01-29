import requests
import json

def get() -> list:
    """
    Loads data from `https://www.bnefoodtrucks.com.au/api/1/trucks`, 
    and returns json object of it.
    """

    bytes = requests.get("https://www.bnefoodtrucks.com.au/api/1/trucks") # data as bytes
    gross = bytes.text # gross data (gross geddit?)
    
    return json.loads(gross) # return pretty data

#print(f"{get()=}")