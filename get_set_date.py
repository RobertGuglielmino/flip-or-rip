import requests
from datetime import date

def get_set_date(set_code):
    response = requests.get(f'https://api.scryfall.com/sets/{set_code}')
    if response.status_code == 200:
        data = response.json()
        return date(*[int(n) for n in data['released_at'].split("-")])
    else:
        print('Error:', response.status_code)
