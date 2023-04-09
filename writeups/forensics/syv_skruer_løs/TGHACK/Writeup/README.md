# Writeup [Syv skruer løs](./README.md)

## Challenge description

**Points: 1000**
_
**Author: Kritt**

**Difficulty: easy**

**Category: forensics**

---

## Writeup

Tre av mange måter å løse oppgaven på:

### 1. Reversing
Reverser .pyc filen, som viser listen (5,2,182,244), som sendes til funksjonen hjerteslag
- Inni hjerteslag lastes index 0 inn, og det blir gjort en BINARY_ADD med 180 -> 185, som lagres i index 0
    ```
    to_ip[0] = to_ip[0] + 180
    ```
- Videre blir det gjort en BINARY_SUBSTRACT på verdien i index 2, med 102 -> 80, som lagres i index 1
    ```
    to_ip[1] = to_ip[2] - 102
    ```
- Til slutt ser vi operasjonen BINARY_TRUE_DIVIDE på index 3 (244) med 2 -> 122, som lagres i index 3
    ```
    to_ip[3] = int(to_ip[3] / 2)
    ```
- I enden av funksjon hjerteslag benyttes den nye to_ip variabelen til å opprette en ny subprocess "ping".
- Programmet pinger altså ut mot IP adressen: 185.80.182.122

### 2. Process monitor
1. Start [process monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon)
2. Legg til filtre:
    - Process name is waddle.exe
3. Start programmet waddle.exe
4. Vent et minutt til process monitor har fått samlet infromasjon om det som waddle.exe foretar seg, for så å stoppe "capture"
5. Ved videre analyse av operasjonene velger vi å fjerne endringer på registrenøkler med følgende filtre:
    - Operation is regopenkey - Exclude
    - Operation is regqueryvalue - Exclude
    - Operation is regclosekey - Exclude
    - Operation is RegEnumValue - Exclude
6. Mot slutten av operasjonslista dukker kall på ping.exe opp.
7. Vi kan også se at waddle oppretter nye prosesser (eks. filter: Operation is Process Create - Include)
8. Under "Details" kolonnen ser vi kommandolinjeparametre som er sendt med, der ligger adressen 185.80.182.122

### 3. Wireshark - Nettverksanalyse
Antagelig den raskeste metoden
1. Start Wireshark, velg capture på "Ethernet" (dobbelttrykk)
2. Start waddle.exe, etter kort stund vil man se mange ICMP pakker som sendes til adresse 185.80.182.122
3. For å verifisere sendingen kan man åpne process exlorer, finne waddle.exe, og være rask ved å høyre klikke på subprosessen som fortløpende dukker opp ved navn "PING.EXE". Åpner man properties vil en se at under kolonnen "image" sin "Command line" dukker den samme adressen opp. Det virker som at waddle.exe starter en ny prosess som pinger 185.80.182.122 med faste intervaller.

Gjør man det om til et flagg:

```
TG23{185.80.182.122}
```
