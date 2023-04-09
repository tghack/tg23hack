# Writeup [passord](./README.md)

## Challenge description

**Author: marie**

**Difficulty: beginner**

**Category: reversing** 

---

## Writeup
Vi har fått en ELF-binary med navn "passord". En fil som sammenligner bruker input med en kode.

Det er flere måter å løse oppgaven på. Den enkleste måten er å bruke "strings". Dette er et kommandolinjeverktøy som vil vise deg ord/sammensetninger som kan minne om ord i binærfilen. I terminalen skriver man "strings passord". Scroll til du finner "TG23{alwH". Merk at flagget vil være spredt på flere linjer, setter man sammen linjene og ignorerer H'ene får man noe som ligner på "TG23{always_be_forgetting}". 

En annen måte man kan løse oppgaven er ved bruk av en dissasembler (f.eks Ghidra eller IDA). Her er det mulig å åpne et pseudokode-view, F5 i IDA. Her kan man se flagget direkte i "qmemcpy" metoden. Man ser også hva filen faktisk gjør; den sammenligner input fra brukeren med tallet "176716". Gir man inn dette tallet til filen når den kjører (./passord) vil man også få flagget ut. 

**Flagg: TG23{always_be_forgetting}**
