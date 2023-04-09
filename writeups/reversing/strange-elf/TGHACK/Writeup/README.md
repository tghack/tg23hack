# Writeup [strange-elf](./README.md)


## Writeup
Oppgaven er et langt rabbit hole om enn følger `main`, med en del forskjellige debug checks, sleep funksjoner m.m. enn vil til slutt komme til en URL `http://strange-elf.chall.tghack.no/qUaK` og tilhørende User-Agent `QuakQuak`, men disse forteller bare at vi har gravd oss langt ned i et kaninhull.
Ser enn i ELF init tabellen, så ser enn en ekstra funksjon `sub_3DFD`, denne setter en `SIGALRM` timer på 500 sekunder som kjører den "faktiske" main funksjonen, som etter litt om og men gjør en request til `http://strange-elf.chall.tghack.no/staged` men User-Agent `flagplz`, gjør enn tilsvarende request så får enn flagget. Annen browsing til nettsiden eller til de rette endepunktene, men feil User-Agent sender enn til 1 av 3 Ductales theme introer.

```
TG23{why all the debug checks?!}
```

### Alternativ løsning
Siden alle strings bruker samme XOR keys `0x13` og `0x37`, kan enn XORe hele binæren med disse 2 verdiene og finne igjen URL'er og User-Agents.