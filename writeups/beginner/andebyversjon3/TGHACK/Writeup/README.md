# Writeup [Andebyversjon3](./README.md)

## Challenge description

**Author: Marie**

**Difficulty: beginner**

**Category: Web**

---

## Write up

### Del 1 - Finn passordet
Klikk på "Vaksine mot fugleinfluensa" på hovedsiden. Her skal man få en alert pop-up med flagget. 

**Flagg: TG23{remember_to_vaccinate_kids}**


### Del 2 - Insecure Direct Object Reference
Logg inn med brukernavn generic-duck og passord som er flagget fra forrige oppgave. I URLen ser du at det er tall. Endre tallet fra 1 til 3 også har du flagget. 

```brukernavn: generic-duck & passord: TG23{remember_to_vaccinate_kids}```

**Flagg: TG23{hogwilde_hogging_the_flagg}**


### Del 3 - SQL injection
Standard SQL-Injection i input-feltet enten på hjemmesiden eller i /search.

Skriv inn: ```' or '1'='1``` så får du flagget

**Flagg: TG23{so_many_ducking_articles}**
