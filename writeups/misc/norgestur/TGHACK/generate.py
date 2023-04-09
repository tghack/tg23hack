import json
import random

with open('post_kart.json', 'r') as fh:
    post_koder = json.loads(fh.readline())

post_koder[' '] = ['0000']

text = 'NEI NÅ HAR DET GÅTT FOR LANGT DONALD VI SKAL PÅ TUR ENTEN DU VIL ELLER IKKE OG DA SKAL VI TIL TGTOTREKRØLLPARANTESHØNETJØNNHEIASLUTTKRØLLPARANTES BARE SÅ DET ER SAGT'

with open('notat.txt', 'w') as fh:

    for letter in text:
        kode = random.choice(post_koder[letter])
        fh.writelines(kode + "\n")

# TG23{HØNETJØNNHEIA}


'''
Nei nå er Ole, Dole og Doffen ute på tur nok en gang og Donlad aner ikke hvor de har blitt av!
De har lagt igjen en lapp med noen tall på som Donald virkelig ikke skjønner seg på. De sa de skulle på tur i Norge, men det er litt uklart hva det har med tallene å gjøre.
Er dette bare et påfunn fra pøbelungene nok en gang, eller har de faktik sagt i fra hvor de er på vei hen? 


Author: solli
'''