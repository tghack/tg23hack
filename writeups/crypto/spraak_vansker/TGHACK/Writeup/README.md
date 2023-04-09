# Writeup [Språk Vansker](./README.md)

## Challenge description
Donald kan være vanskelig å forstå til vanlig, men nå har han gått helt av skaftet. Det er ikke så lett å si hva som har skjedd med Donald, men det går rykter om at Magica har vært involvert.

Ole, Dole og Doffen har i hvert fall vært behjelpelige med å notere hva Donald har sagt, men har ikke funnet noe i hakkespettboken om dette. Kan du hjelpe dem med å tyde hva Donald sier?

Nak? Naknaknaknak Naknak nak? Naknak Naknaknak Nananak Nak Naknak Nak. Naknak Nanak Naknaknak Nananak Nananak Nak Naknak Nananak Naknak naknak Naknak Naknak. Naknaknak Nak? Naknaknak Nak? Nananak Nak Naknak Naknak Naknak naknaknak Naknaknak Nananak Naknak Nak. Naknak nak? Naknak nanak Naknaknak Nanananak Naknak nak? Naknaknak Nak? Nananak Nak Naknak Nanak Naknaknak Naknak Nananak Nak Nak? nak! Naknak Nanak Naknak Naknaknak Naknak Naknak. Naknak Nanananak Naknak Nanak Nananak naknak Nananak Nak Naknak Naknak Naknak naknaknak Naknaknak Nananak Nananak Nak Naknak naknaknak Naknak Naknaknak Nananak Nak Naknak Nananak Naknaknak Nananak Naknaknak Naknak. Naknaknak Nak? Naknak nak? Nananak Nak Naknak Naknak Naknak naknaknak Naknaknak Nananak Naknak Nananak Naknak Nanak Naknak nak. Naknak Nak? Naknak nak? Naknak naknak Naknaknak Nanananak Naknak nak? Naknak nak. Nananak Nak Naknak nak! Naknak Nanak Nananak Nak Naknak Nak? Naknaknak nak? Nananak Nak Naknaknak Nanananak Naknak Naknak. Nanananak Naknaknaknak Nananak Nak nak? Nak? Nak? Naknaknak Nanananak Nananak Nanananak Nanananak Naknaknak nanak nak? Nanak Naknaknak nak? Naknak Nanak Naknak Nanananak Naknak nanak nak? naknaknak nak? Nanak Naknaknak nak? Naknak Nanak Naknak Nanananak Naknak nanak nak? naknaknak Naknak Naknak. Naknak nanak Naknak nanak Naknak nak? nak? naknaknak Naknaknak Nanananak Naknak naknaknak Naknak nak! nak? naknaknak Naknak Nak? Naknak nak? Naknaknak Nak? nak? naknaknak Naknaknak Nak Naknak naknak Naknak nak? Naknak Naknak. Naknak nak? Naknaknak Nananak nak? naknaknak Naknak Nanak nak? naknaknak Naknaknak Naknak Naknak Nanak Naknak nak? Naknaknak Nananak Naknak nak? Naknaknak nak!

**Points: 1000**

**Author: AresDiode**

**Difficulty: easy**

**Category: crypto** 

---

## Writeup

I denne oppgaven får vi en lang tekst som er kryptert med en Substitution Cipher, DuckSpeak. DuckSpeak kan lett gjenkjennes fordi alle ord er bygget opp av Nak og Naknak. Om man ikke kjenner igjen cipheren så er det verktøy som [Decode.fr](https://www.dcode.fr/cipher-identifier) sin cipher identifier som kan hjelpe. Så fort man vet hvilken cipher det er så er det bare å finne en decoder for den, og et kjapt google søk gir oss [DuckSpeak decoder](https://www.dcode.fr/nak-nak-duckspeak). Så er det bare og lime inn teksten og få ut flagget.



And then... Whoop whoop, I got the flag!

```
TG23{Quack_Quack_ikke_som_det_pleier_a_vaere}
```
