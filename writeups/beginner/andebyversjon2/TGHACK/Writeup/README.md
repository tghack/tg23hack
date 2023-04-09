# Writeup [Andebyversjon2](./README.md)

## Challenge description

**Author: Marie**

**Difficulty: beginner**

**Category: Web**

---

## Write up

### Del 1 - Robots.txt
I oppgaven har Andeby kommune fått en bekymringsmelding med et bilde av Petter Smarts Lille Hjelper (lyspæra), med bildeteksten "Whirrrrr, clank clank, beep beep, bloop bloop."

I følge ChatGPT er dette noe en robot sier. Så her vil vi frem til at man skal besøke /robots.txt. I robots.txt får vi tips om /offlimits. Vi besøker /offlimits og får flagget.

**Flagg: TG23{there_are_hidden_ducks_on_the_website}**


### Del 2 - flag.png
I del 2 får Andeby kommune en melding om at noe "skurrer" med bilde på nettsiden. Åpner man "inspiser" verktøyet kan man se at bildet er hentet fra mappen static/ducks. I forrige flagg fikk vi også tips om at det finnes gjemte ender på nettsiden. Her kan man altså endre bildet i "inspiser" verktøyet til for eksempel flag.png, og fra dette bildet tyde flagget. 

PS: Det finnes flere ender 

**Flagg: TG23{WE_GOT_ALL_THE_DUCKS}**


### Del 3 - /secret 
Her får vi vite i oppgaven at BG AS (B-Gjengen AS) kanskje har gjemt en hemmelighet på en "secret" plass. Her refererer secret til et directory / en mappe. Vi så også i del 2 at bildet av Onkel Skrue ble hentet fra en url. Denne urlen kan man bruke til å utføre et Local file inclusion angrep hvor man endrer urlen til å hente andre mapper og filer fra nettsiden. Vi er altså interessert i mappen secret som ligger i rot-mappen til nettsiden, og tekstfilen flag.txt. Endelig path blir da:

andebyversjon3.chall.tghack.no/static/ducks/?name=../../secret/flag.txt

**Flagg: TG23{we_used_chatgpt_to_create_this_website}**
