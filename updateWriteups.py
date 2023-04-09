#!/usr/bin/env python3
from os import listdir, makedirs, walk
from os.path import isfile, join, exists, basename
text = """
# TGHACK 23
> Writeups and challenges resources for TGHACK23


## Table of content
- [afk](#misc)
- [beginner](#beginner)
- [coding](#coding)
- [crypto](#crypto)
- [forensics](#forensics)
- [misc](#misc)
- [osint](#osint)
- [pwn](#pwn)
- [reversing](#reversing)
- [web](#pwn)

---

## Writeups

"""

for category in listdir("./writeups"):
    if category.startswith(".") or isfile(category):
        continue
    text += f'### {category}\n'
    for chall in listdir(f'./writeups/{category}'):
        text += (f' - **{chall}**\n')
        print(text)
        for writeup in next(walk(f'./writeups/{category}/{chall}'))[1]:
            url = f'/writeups/{category}/{chall}/{writeup}'.replace(' ', '%20')
            text += f"\t - [{writeup}]({url})  \n"
            print(text)

open('README.md', 'w').write(text)