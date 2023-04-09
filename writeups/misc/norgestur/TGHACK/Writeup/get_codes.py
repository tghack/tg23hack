import requests as r
import string
import urllib.parse
import json

URL = 'https://adressesok.posten.no/api/v1/postal_codes.json?'


postal_map = {}

for letter in string.ascii_uppercase + "ÆØÅ":
    safe_letter = (urllib.parse.quote(letter, safe=""))
    payload = f"postal_code={safe_letter}*&per_page=2000"
    postal_info = r.get(URL+payload).json()['postal_codes']

    postal_map[letter] = []

    for place in postal_info:
        if place['city'][0] == letter:
            valid_code = place['postal_code']
            postal_map[letter].append(valid_code)
            print(f'{letter} / {place["city"]}')


with open('post_kart.json', 'w') as fh:
   fh.writelines(json.dumps(postal_map)) 




    