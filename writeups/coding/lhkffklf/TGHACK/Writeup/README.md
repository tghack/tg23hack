# LHKFFKLF (Lille hjelpers kyberforum for kybernetiske livsformer)

## Challenge description

**Author: Thhethssmuz**

**Difficulty: challenging/hard**

**Category: coding/web**

**Description Norwegion**:
> Lille Hjelper er lei av forskjellige ikke-kybernetiske enheter som troller forumet hans, så han prøvde å lage en omvendt captcha for å låse dem ute. Som en kybernetisk enhet selv fant han imidlertid at alle metodene var trivielle, og derfor har han vervet deg, et menneske, til å trollsikre nettstedet hans.

**Description English**:
> Little Helper is tired of various non-cybernetic entities trolling is forum, so he tried making a reverse captcha to lock them out. However, as a cybernetic entity himself he found all the methods to be trivial, thus he has enlisted you, a human, to troll-proof his site.

## Writeup

This write-up is in English, however, the challenges themself as well as the flags are in Norwegian.

### 1

You are presented with a challenge that is a mathematical equation of the form `a / b + c^d`. You need to solve this and input the solution into the input field, however you only have 2 seconds before a new one is generated, making it about impossible for a human to solve in time.

Though the challenge is plain text so you can solve this pretty easily by using the browser console and `eval`, only thing you need to lookout for is that the `^` operator is not the power operator in JavaScript, so you need to replace that with `**` before passing it to `eval`:

```js
document.querySelector('#challenge-answer').value = eval(document.querySelector('#challenge-content').innerText.replace('^', '**')); document.querySelector('.btn').click();
```

Solution: `TG23{mennesker_er_ikke_gode_i_hoderegning}`

### 2

Similar to #1, however this time the challenge is an image, which makes the challenge significantly harder. Note that you can probably not solve the challenge in the browser console alone, you will have to use external tools.

At this point you will probably want to ditch the browser entirely, and connect directly to the websocket yourself, as that will make your life much easier. Once connected you will receive a challenge message every second with a base64 encoded png image and at that point you can solve this in at least 2 different ways:

1. The image has metadata which contains the equation.
2. You can use an image to text tool like `tesseract`.

See the test folder for how to do both of these in bash :D

Solution: `TG23{bare_i_tilfellet_mennesker_kan_lese_utf8}`

### 3

Here the challenge is a qrcode. Should be pretty straightforward, parse the qrcode, but you only have 5 seconds.

Solution: `TG23{mennesker_kan_hvertfall_ikke_lese_qr_koder}`

### 4

This time the challenge is to count golden pixels in an 100x100 image. The image itself consist mostly of random noise, however there is a sizeable number of "golden pixels", i.e. pixels with the colour value of #FFD700, and you only have 5 seconds before a new image is generated.

This should be solvable in the browser console if you are familiar with the canvas API, though I must admit I have not tried this myself atm., As like the other challenges there is nothing stopping you from connecting to the websocket manually and that is the approach I have used in the tests.

Solution: `TG23{menneskers_øyne_har_en_dpi_på_170_så_dette_burde_være_umulig}`

### 5

Here the challenge is a midi file, which for those unfamiliar is a musical notation format. You can easily play this file if you have a midi player, and as long as you are not too entranced by the Duck Tales theme, then you should realize that something is a little off. This along with the challenge text "Music in high velocity" is all you get in terms of hints.

A midi player is provided on the page itself, however, the file is some 40 seconds long and you only have 10 seconds before the player resets and loads a new seemingly identical file. Which means you can only hear the first 10 seconds of the song as long as you are not manually forwarding or hacking the page's JavaScript.

To solve this you'll have to parse the midi events somehow and extract the velocity values for all the `note-on` and `note-off` events. Then you'll find a hidden message in the least significant bit of the note velocities. However to emphasize the difference there are only two note velocity values `0x5f` and `0x20`, making the difference very audible.

Solution: `TG23{mennesker_har_heller_ikke_god_hørrsel}`

### 6

You are presented with a 10x10 grid of images of either Donald Duck or Donald Trump, and you have to select all the ducks. Each image is only 32x32 so selecting all of them in time is going to require some precision mouse work and inhuman speed, especially when you consider that you only have 5 seconds before a new grid is generated.

The grid it self is only one single 320x320 image and should not contain any exploitable metadata. However, there is only 6 images of each Donald, thus if you split the image into its constituent parts then you should be able to identify them by shasum. Although there are also drastic colour differences between the set of Donald Ducks and the set of Donald Trump so some kind of average colour differentiation should also be possible.

**NOTE** that I have not yet solved this

Solution: `TG23{hvor_god_er_menneskers_donald_klassifiserings_algoritme}`
