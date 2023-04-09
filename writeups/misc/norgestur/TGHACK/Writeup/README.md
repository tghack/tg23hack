# Writeup [Norgestur](./README.md)

## Challenge description

**Author: solli**

---

## Writeup

Ettersom det er nevnt at dette er en tur i Norge skal det gi mening å tolke tallene som postnummer. Søker man opp 1 og 1 tilfeldig ser man kanskje ikke noe mønster, men om man går nedover lista og setter de over hverandre vil den første karakeren i hvert ord danne en setning. Kodene 0000 som er lagt inn skal også gi en pause mellom hvert ord, slik at det skal være enklere å tenke seg at dette kan være ord. 
For å enkelt dekode dette kan man hente ut alle verdier og postnummer fra posten.no på noen sekunder, og gå gjennom disse for å kunne raskt dekode tallene til flagget. Men, det er også mulig å gjøre manuelt, men det tar litt tid. 


Hente ut bokstav til postnummer:

```py
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
```

Deretter dekode teksten ved hjelp av mappingen som nå ligger i post_kart.json:

```py
import json

with open('post_kart.json', 'r') as fh:
    post_koder = json.loads(fh.readline())

post_koder[' '] = ['0000']

with open('notat.txt', 'r') as fh:
    notat = [a.strip() for a in fh.readlines()]

for kode in notat:
    for bokstav in post_koder:
        for test_kode in post_koder[bokstav]:
            if test_kode == kode:
                print(bokstav, end='')
```

Tekst: `NEI NÅ HAR DET GÅTT FOR LANGT DONALD VI SKAL PÅ TUR ENTEN DU VIL ELLER IKKE OG DA SKAL VI TIL TGTOTREKRØLLPARANTESHØNETJØNNHEIASLUTTKRØLLPARANTES BARE SÅ DET ER SAGT`

```
TG23{HØNETJØNNHEIA}
```
