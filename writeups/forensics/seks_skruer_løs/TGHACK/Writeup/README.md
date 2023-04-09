# Writeup [Seks skruer løs](./README.md)

## Challenge description

**Points: 1000**
_
**Author: Kritt**

**Difficulty: easy**

**Category: forensics**

---

## Writeup

Denne oppgaven vil også kunne løses på flere måter.

Først, for å finne filen ved navn passord:
- Man kan gjøre søk i stien C:/Users/ etter passord
- Powershell: Get-Childitem -path C:\Users\ -Recurse -Include passord*

Kommandoen viser en fil i C:\Users\User\Documents med en uvanlig filending: passord.txt.wad

For å få mer innsikt i hva som skjer når waddle.exe finner en slik fil, kan man kjøre [process monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon), lage en egen passord.txt fil med vilkårlig innhold under C:\Users\, og legge til følgende filtre:
- Process name is waddle.exe
- Path contains passord.txt

Når man da kjører waddle.exe vil det etter kort stund dukke opp operasjoner som viser at programmet leser og skriver til passord.txt, før det til slutt endrer navnet på fila til ".wad".

Om man enten velger å forsøke å reversere hele pyc fila, basert på [dokumentasjonen](https://docs.python.org/3.10/library/dis.html), eller bare leser på intruksjonene i "man.txt" generert fra forrige oppgave, vil man fort se at det gjennomføres en XOR operasjon. 

En annen string som også dukker opp er "bXludGVyCg==" som lagres i variabelen "key". Den benyttes så i XOR operasjonen.

Ved dynamisk testing, vil man fort se at programmet bare gjør endringer på filer som heter passord.txt. Ved å fjerne ".wad" endingen på den orginale passordfila, og kjører waddle.exe, vil den dekodes med "key", og det som gjenstår i fila er flagget.

```
TG23{verdensRikesteMann12K}
```
