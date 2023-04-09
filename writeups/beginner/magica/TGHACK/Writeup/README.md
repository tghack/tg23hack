# Writeup [magica](./README.md)

## Challenge description

**Author: marie**

**Difficulty: beginner**

**Category: Reversing** 

---

## Writeup
I oppgaven får vi en ELF-binary med navn "magica". En fil som sammenligner bruker input med et passord.

Det er flere måter å løse oppgaven på. Her kan man bruke linux kommandoverktøyet "ltrace" (obs: dette er en dynamisk analyse av filen, det vil si at filen kjører - altså ikke bruk den på virus eller mistenkelige filer). Ltrace vil vise deg systemkall som gjøres av binærfilen. Kjører du ltrace vil du kunne se hva brukerinputet blir sammenlignet med og dermed vil du lære det hemmelige passordet og kan bruke dette til å få tak i flagget.


En annen måte er ved bruk av disassembler. Her kan du gå i pseudokode-view ved bruk av F5 (på IDA). Gå til "strcmp" metoden. Her ser vi at brukerinput (a1) sammenlignes med S2. Leter man litt i koden kan man se at S2 består av S2 + karakterer fra v10. Finn S2 og v10 og putt de sammen. Da får man den hemmelige koden som kan lede til flagget om man kjører filen. Eventuelt kan man se at den hemmelige koden er v1 som er en base64 encoded string. Her dekodes v25. Finner du v25 kan du kjøre base64 stringen i cyberchef selv og få flagget. 

**Flagg: TG23{1_l1k3_3nc0d1ng}**