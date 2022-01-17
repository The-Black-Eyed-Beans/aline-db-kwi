import api
import requests
import os

from dotenv import load_dotenv

load_dotenv()


# Function to login to the API to get the Bearer Token
def get_bearer():
    info = {'username': os.getenv('ALINE_USERNAME'), 'password': os.getenv('ALINE_PASSWORD')}

    try:
        response = requests.post(api.get_api() + '/login', json=info)

        if response.status_code in range(200, 301):
            return response.headers['authorization']
    except Exception as ex:
        print(ex)
    return None
