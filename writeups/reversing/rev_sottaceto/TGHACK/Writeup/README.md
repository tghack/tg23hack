# Writeup [Fancy task name](./README.md)

## Challenge description


---

## Writeup
Vi får 2 filer, `Sottaceto1.txt` inneholder et Python `pickle` object som er base64 enkodet, og `Sottaceto2.txt` inneholder output fra Python `dis` gjort på det som virker å være en klasse.

Forsøker enn å laste objectet får enn bare følgende feilmelding:
```
AttributeError: Can't get attribute 'Flagchecker' on <module '__main__' (built-in)>
```
så klassen heter `Flagchecker`.

Basert på output fra `dis` kan vi da rekonstruere `Flagchecker` klassen:
```python
class Flagchecker:
    def __init__(self):
        self.FLAG = []
    def check_flag(self, user_flag):
        if isinstance(user_flag, str):
            user_flag = user_flag.encode()
        for a, b in zip(user_flag, self.FLAG):
            if enc(a) == b: continue
            return False
        return True
    def enc(c):
        return ((c^0x13) << ((c^0x37) & 0xF ))
```

Vi får da en enkel crypto loop vi kan bruteforce. Vi henter det faktiske flagget fra `pickle`:
```python
import pickle, base64

class Flagchecker:
    def __init__(self):
        ....

FLAG = pickle.loads(base64.b64decode("gASVfwAAAAAAAACMCF9fbWFpbl9flIwLRmxhZ2NoZWNrZXKUk5QpgZR9lIwERkxBR5RdlChNOAJLVE0gBE0AAkoAgAYATbgDTYAITQAGTYAZTYAxTYAITQAHSgCABwBKAPgDAE0AAk2AGU0gDk0AAk2AGUtkTQACTYAITSAMTbgDSgC4AQBlc2Iu"))
print(FLAG.FLAG) # [568, 84, 1056, 512, 425984, 952, 2176, 1536, 6528, 12672, 2176, 1792, 491520, 260096, 512, 6528, 3616, 512, 6528, 100, 512, 2176, 3104, 952, 112640]
```

og lager et enkelt solve-script:
```python
def enc(c):
        return ((c^0x13) << ((c^0x37) & 0xF ))

from string import printable
PT_FLAG = []
for f in FLAG.FLAG:
    PT = []
    for c in printable:
        enc_c = enc(ord(c))
        if enc_c == f:
            PT.append(c)
    PT_FLAG.append('[' + '|'.join(PT) + ']')
print(''.join(PT_FLAG))
```
Bruteforcen gir en kollisjon med `{` og ` `, men ellers er flagget lesbart: `TG23{d1s p1ckl3 b3 w31rd}`