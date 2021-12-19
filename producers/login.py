import requests
import os

from dotenv import load_dotenv

load_dotenv()


# Function to login to the API to get the Bearer Token
def get_bearer():
    info = {'username': os.getenv('ALINE_USERNAME'), 'password': os.getenv('ALINE_PASSWORD')}
    response = requests.post('http://localhost:8070/login', json=info)

    return response.headers['authorization']
