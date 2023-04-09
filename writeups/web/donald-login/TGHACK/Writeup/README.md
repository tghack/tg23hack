# Writeup [Fancy task name](./README.md)

## Challenge description

**Author: solli**

---

## Writeup

### Flag 1
Etter login får man opp at man er for treg.. Noe som ikke helt gir mening.
Dersom du sjekker hvordan du har blitt logget inn i cookies ser du at du i alle fall har fått en cookie. Så det er kanskje her Petter smart har gjort noe merkelig.

Cookien burde være klar base64, men noe som ikke stemmer helt. Reverse stringen så får du dekodet første steget, som gir 3 nye biter.
Disse bitene kan dekodes hver for seg, og vil gi deg tre forskellige outputs. 

Første delen er kun tall, noe som cyberchef f.eks vil gjennkjenne som et timestamp. Øker man denne verdien nok vil du kunne være i "fremtiden", og med det komme forbi det som virker som første sjekk av at du er for treg.


### Flag 2
Etter login vil du kunne se at det er et regnestykke som regnes ut. Dette er knyttet opp mot del 2 av cookien, og manipulering av verdier vil gjennspeiles på nettsiden.
Videre gir headers innblikk i at dette er en python server: Werkzeug/2.2.3 Python/3.8.10. Kan da f.eks teste med command injection på del 2 av cookie for å sjekke om regnestykket f.eks regnes ut ved hjelp av eval() eller exec().

Kan da teste med f.eks command injection:
__import__('subprocess').check_output(['ls', '-la'])
__import__('subprocess').check_output(['cat', 'flag_35879325.txt'])

