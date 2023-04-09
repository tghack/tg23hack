# Writeup [To skruer løs](./README.md)

## Challenge description

**Points: 1000**
_
**Author: Kritt**

**Difficulty: easy**

**Category: forensics**

---

## Writeup

Som fortsettelse fra forrige oppgave, i process explorer, etter å ha gått inn i properties for python3.10.exe programmet vil man under "Image" kunne se fillokasjonen til programmet.
    - Current directory: C:\Users\User\Documents\Visual Studio 2022\

Ved å bruke file explorer til den mappa finner man pythonfila "boyd.py".
Etter å åpne den hinter den om en tjeneste som heter "Task scheduler" hvis du skriver inn en spesifik string til programmet.

Åpner man task scheduler, og går ned til "Active tasks", ser man en task med navn "B.O.Y.D". Et dobbelttrykk på den viser mer informasjon, og under "General" fanen er det et description felt som inneholder en base64 enkodet string.

Ved å dekode stringen får man flagget.

```
TG23{duck_m4_0v3rl3v3_duck_må_b357}
```
