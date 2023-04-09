# Writeup [Borte for alltid](./README.md)

## Challenge description

**Category: forensics** 

---

## Writeup

Mailen har 2 attachment. En diary og et bilde. Ettersom diary er kryptert med AES-ECB er det ikke mulig å åpne fila så da må man jobbe med bildefila. Emailen inneholder ", but I trust that if you are the least bit concerned, you will be able to find it.". Dette er et hint til at man skal finne info ved å extracte LSB ("least bit") dataen fra bildet. Sjekker man plane 0 i stegsolve ser man litt rare greier på toppen av bilde (altså bit 0). Ved å bruke "extract data" i stegsolve på bit 0 i RGB, går man ut en zip fil. Den kan man kjøre binwalk på og få ut key.txt fila. Inni den er nøkkelen for å dekryptere diary.enc. Dette kan gjøres i f.eks. cyberchef. Gjør man dette får man en docx fil. Inni fila ser vi dagboka til Onkel Skrue. Siste side inneholder base64 enkoda versjonen av flagget.

Nøkkelen til diary.enc:
```
l3iHnwJe4uKFQPuXAUDOAfGwrJJKkHBu
```


Dekrypterer diary.enc og finner følgende i diary.docx:
```
VEcyM3tuM3dfNGR2M243dXIzNV80aDM0ZCF9IA==
```
som blir dekodet til:
```
TG23{n3w_4dv3n7ur35_4h34d!}
```

