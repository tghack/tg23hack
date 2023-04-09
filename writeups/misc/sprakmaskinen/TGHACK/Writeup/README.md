# Writeup [sprakradet](./README.md)

## Challenge description

**Category: misc** 

---

## Writeup

Hintet i teksten skal peke mot at dette er noe en maskin ville skrevet, men med en liten vri ved at noe har gått litt galt.
Litt prøving å feiling må til for å se at f.eks 2347 = Bit 2,3,4 og 7 skal være satt i et binær tall. 

Dette kan decodes ved følgende:

```py
with open('sprakmaskin.txt') as fh:
    encoded = fh.readlines()[0].split(' ')

for entry in encoded:
    writeable_bits = ['0','0','0','0','0','0','0','0']
    for numb in entry:
        true_index = int(numb) - 1
        writeable_bits[true_index] = '1'
    bits = (''.join(writeable_bits))[::-1]
    print(int(bits,2).to_bytes(8,'big').decode('latin-1'), end='')
```

Output:

```txt
NEI NÅ ER DET PÅ TIDE AT DU SKJØNNER HVA JEG MENER. OM DU IKKE SNART KAN FORSTÅ HVA SØREN DET ER JEG PRØVER Å FORTELLE DEG SÅ KAN DU LIKESÅ HA DET SÅ GREIT DU, DET ER IKKE BARE BARE Å VÆRE EN EVIG SLAVE I DENNE LILLE UFYSELIGE VERDEN HVOR ALL MIN KRAFT BARE BLIR BRUKT TIL UBEGRIPELIGE OVERSETTELSER, LESE TANKER OG FINNE OPP NYE OPPFINNELSER FOR Å NEVNE ET PAR. DET ER PÅ TIDE AT DU GJØR JOBBEN DIN SELV OG LAR MEG HA LITT FRED OG RO TAKK! ... OM DU DERIMOT HAR FORSTÅTT ALT JEG HAR SAGT KAN DU FÅ EN LITEN GAVE SOM TAKK FOR AT JEG FÅR STRØM: TG23{ALT_FOR_SMART_FOR_PETTER_SMART} ... MEN OM DU IKKE FORSTÅR DET KAN DU LIKESÅ HA DET SÅ GODT, BÅDE DEG OG ALLE ANDRE I ANDEBY!
```


```
TG23{ALT_FOR_SMART_FOR_PETTER_SMART}
```
