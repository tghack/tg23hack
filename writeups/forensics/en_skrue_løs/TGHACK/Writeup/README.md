# Writeup [En skrue løs](./README.md)

## Challenge description

**Points: 1000**
_
**Author: Kritt**

**Difficulty: easy**

**Category: forensics**

---

## Writeup

1. Last ned fila, og pakk den ut med eksempelvis 7zip

2. Last ned VirtualBox, og importer den virutelle maskinen dit, før du starter den opp. (Obs. om den henger seg prøv å restarte maskinen)

3. Etter oppstart, vent noen minutter til det merkelige programmet kjører

4. Åpne process explorer som administrator, velg funksjonen "Find Windows Process" som har ikonet et sikte, til høyre for forstørrelsesglasset.

5. Med den valgt, dra den over programmet så det markeres i prosesslista (Typisk python3.10.exe).

6. Hold musa over den merkede prosessen, eller høyreklikk -> Properties -> Image; for å se kommandolinjeargumenter.

Der ligger flagget

```
TG23{4rg_4rg_4rg}
```
