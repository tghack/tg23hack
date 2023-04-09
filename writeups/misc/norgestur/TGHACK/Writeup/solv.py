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