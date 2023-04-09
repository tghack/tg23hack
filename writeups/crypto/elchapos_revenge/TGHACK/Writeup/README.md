# Writeup [El Chapo's Revenge](./README.md)

## Challenge description

Petter Smart sendte meg nylig en melding på FAX om at Lille Hjelper hadde funnet en måte å knekke krypteringen min på.
Jeg endret krypteringen min for å være resistent mot slike angrep, og satte opp en nettside for å demonstrere min nye utra-sikre kryptering! Du finner aldri flagget!


**Points: 1000**

**Author: Sithis**

**Difficulty: hard**

**Category: crypto** 

---

## Writeup

Ved å inspisere koden kan vi gjøre oss noen observasjoner:

1. noncen i `encrypt`-funksjonen blir generert basert på de første 16 tegnene i plaintexten.
2. vi kan kryptere både privatnøkkelen og flagget
3. vi vet hvilke bytes den PEM-enkodede privatnøkkelen starter med (`-----BEGIN PRIVATE KEY-----`)

Vi kan kryptere en annen plaintekst som starter på det samme som privatnøkkelen, som gjør at det vil ha samme nonce og derfor cipherstream. Vi kan da XOR-e dette med ciphertexten til privatnøkkelen for å få plaintexten til privatnøkkelen.

Når vi krypterer data får vi bare x-koordinatet til P, men vi kan tilbakehente y-koordinatet ved hjelp av Tonelli-Shanks-algoritmen (som lar deg regne ut kvadratrøtter over endelige kropper).

Alt dette satt sammen gjør at vi kan dekryptere flagget.

Se solve script for konkrete detaljer på hvordan dette gjøres :)

