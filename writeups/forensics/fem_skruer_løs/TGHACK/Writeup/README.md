# Writeup [Fem skruer løs](./README.md)

## Challenge description

**Points: 1000**
_
**Author: Kritt**

**Difficulty: challenging**

**Category: forensics**

---

## Writeup

Det er mange måter å løse denne oppgaven på, her er en måte inspirert av [1]:

1. Programikonet hinter om kompilering fra Python.

2. Konverter fra EXE til PYC med pyinstxtractor.py (https://github.com/extremecoders-re/pyinstxtractor)
    - Henter ut innholdet i en pyinstaller generert exe fil
    - python pyinstxtractor.py <filnavn>

3. Man får så generet en hel liste med filer, den interessante for oss er waddle.pyc. Denne kan manuelt dekodes med følgende kodesnutt lagret i fila manuell.py:

```
import sys
import dis, marshal
pyc_path = sys.argv[1]
with open(pyc_path, 'rb') as f:
    # First 16 bytes comprise the pyc header (python 3.6+), else 8 bytes.
    pyc_header = f.read(16)
    code_obj = marshal.load(f) # Suite to code object
dis.dis(code_obj)
```

    - python manuell.py waddle.pyc > man.txt

4. I man.txt ser en 3 distinkte kolonner.
    - Seksjoner: hver seksjon representerer en linje i det originale python programmet
    - Instruksjoner: Instruksjonen som gjennomføres
    - Parametre: Parametre til instruksjonen
    - For mer informasjon om dekryptering av instruksjonene: https://docs.python.org/3.10/library/dis.html

5. Koden har noen grupper med stringer som antyder søking etter filer.
    - find, passord.txt, C:/Users/
    - find ser vi at er en funksjon som tar imot parametrene passord.txt og C:/Users/, for så å bruke python biblioteket "os" og funksjonen "walk" til å traversere i det man kan anta at "path" tilsvarer C:/Users/.
    - Under traversering blir biblioteket fnmatch med tilsvarende funksjon brukt på "name", som sammenlignes med "pattern" (som vi kan anta er passord.txt). 

6. Vi legger til TG23 til filnavnet og skaper flagget vårt

```
TG23{passord.txt}
```

[1] https://betterprogramming.pub/analysis-of-compiled-python-files-629d8adbe787
