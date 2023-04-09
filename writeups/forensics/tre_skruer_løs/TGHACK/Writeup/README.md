# Writeup [Tre skruer løs](./README.md)

## Challenge description

**Points: 1000**
_
**Author: Kritt**

**Difficulty: easy**

**Category: forensics**

---

## Writeup

Description feltet i "B.O.Y.D" tasken i task scheduler hinter om HKCU registeret. 
Google søk etter "continuous run program from registry", eller lignende sjargonger vil henviste til flere mapper i registeret. Ett av dem er "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run".

Programmet "Registry Editor" kan benyttes for traversering i windows registeret. Ved å gå til HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run finner man flere merkelige nøkler. 

Spesielt "TODO_BOYD" skiller seg ut med en referanse til forrige oppgave.
I dens "Data" finner man en base64 enkodet string som kan dekodes til flagget.

```
TG23{duck_1_run_3r_574ndh4f716}
```
