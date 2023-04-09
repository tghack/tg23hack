# Writeup [Fancy task name](./README.md)

## Challenge description

**Points: 1337**

**Author: PewZ**

**Difficulty: n00b/easy/challening/hard/crazy**

**Category: crypto/RE/pwn..** (optional, several may be added if suitable)

---

## Writeup

Dette er i bunn og grunn en ganske klassisk bildegjennkjenningsoppgave, med en liten twist på slutten for å produsere et flagg. De som har vært borti MNIST datasettet har nok en liten fordel, siden det er samme dimensjonene på bildene som det bruker. Datasettet jeg har brukt er tross alt den balanserte EMNIST hvor jeg har tatt bort litt fra test datasettet. For å løse det må man:

1. Trene en modell på train.csv datasettet, som man godt også kan se at accuracy mot treningssettet burde ligge godt oppimot 95% + tipper jeg. Har ikke fått den til å lage feil string til meg enda selv, men det kan skje hvis man enten overfitter modellen eller har en helt elendig algoritme kjørende. 

1. Siden det bare skal telles hvor mange av hver klasse det er, så gjør man egentlig bare det med modellen man har lagd. Predict alle bildene, og lagre opptelling av de på en fornuftig måte

1. Hvis man ikke har eksperimentert med mapping.txt må man det i hvert fall nå. Man ser fort at det første kollonnen i filen representerer label i train.csv, mens det andre representerer ASCII koden til det. Map derfor alle labels fra label til ASCII.

1. Gjør en replace av nå tallene fra ASCII 7, 8, 9 med {} og _ som beskrevet i oppgaveteksten

1. Rangsjer hver klasse fra mest til minst, og man får flagget ut

Som sagt så kan man angripe denne oppgaven som man angriper MNIST oppgaver. [Her](https://towardsdatascience.com/image-classification-in-10-minutes-with-mnist-dataset-54c35b77a38d) kan du lese en ganske stadard løsning på det. Det går an å kjøre hva man vil her egentlig, men det er nok en fordel å kjøre en konvulusjon av noe slag med en fungerende ML algoritme (typ CNN), for det er tross alt en bildegjennkjenningsoppgave.

Det eneste som er anderledes er at bildene og labels kommer i et litt rart format som enklest kan løses med å skrive noe som:

```python

import pandas as pd
training_letter = pd.read_csv('train.csv')

train_y = np.array(training_letter.iloc[:,0].values)
train_x = np.array(training_letter.iloc[:,1:].values)

train_x = train_x.reshape(train_x.shape[0], 28, 28, 1)

```
Hvor train_y er labels og train_x er bildet



Etter trening, og hvis man følger eksempelet fra towards data science kommer man til slutt til predictions hvor man kan skrive noe som dette for å få alle preictions:

```python
predictions = []
predictions.append(model.predict(x_test.reshape(len(x_test), 28, 28, 1)))
```

Til slutt er det bare å argmaxe alle predictions, lage en fornuftig måte å lagre resultatene på, sortere de etter antall og bytte ut string fra oppgaveteksten og lage flagget til slutt:
```python
pred_dict = {}
for p in predictions[0]:

    print(p)
    argmax = np.argmax(p)

    print(argmax)

    if argmax not in pred_dict:
        pred_dict[argmax] = 0
    pred_dict[argmax] += 1


pred_arr = []
for k, v in pred_dict.items():
    pred_arr.append( (k, v))

pred_arr.sort(key=lambda a: a[1], reverse=True)

with open("mapping.txt") as f:
    data = f.readlines()

translate_dict = {int(d.split()[0]):int(d.split()[1]) for d in data}

final_string = ""
for a in pred_arr:
    character = chr(translate_dict[a[0]])
    if character == "7":
        character = '{'
    if character == "8":
        character = '}'
    if character == '9':
        character = '_'
    final_string += character
print(final_string)

```

Til slutt vil man få flagget sitt i klartekst:

```
TG23{AI_NDEBY}
```
