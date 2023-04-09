# Writeup [bilde-opsec 2](./README.md)

**Author: solli**

---

## Writeup

Lignende oppgave "bilde-opsec" så har denne et bilde skjult i seg. som ikke er synlig når det først åpnes.
I motsetning til første oppgave så er det ikke like åpenbart at det er ekstra data. Men det kan merkes ved at exiftool sier det er noe trailing data etter PNG IEND chunk, som tilsier at det er mer data i fila enn det burde være.


Ved hjelp av binwalk kan man extracta alle de forskjellige IDAT chunkene fra PNG bildet. Dette er zlib komprimert data som inneholder de forskjellige pixel verdiene til bildet. Den siste av disse bitene kan være interessant å ta en titt på ettersom det trolig er den som er etter IEND chuncken. For å displaye innholdet i en slik fil kan f.eks Pillow benyttes i python.

Størrelsene i bildet kan tolkes utifra at bildet sine opprinnelige verdier er 1920x930, hvor det da manlger 150px høyde for å ha en relativ normal oppløsning på en skjerm.

```py
import zlib
from PIL import Image

with open('extracted_data.zlib', 'rb') as fh:
    idat_data = fh.read()

# Decompress the IDAT data
decompressed_data = zlib.decompress(idat_data)

# Create a new image object with the decompressed data
idat_image = Image.frombytes("RGB", (1920, 150), decompressed_data)

# Display the IDAT image
idat_image.show()
```

Flag: `TG23{dette_finner_nok_ikke_donald}`