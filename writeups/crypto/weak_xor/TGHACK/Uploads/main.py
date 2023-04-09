import os
from flag import flag
key = os.urandom(2)


def xor(data, key):
    return [data[i] ^ key[i % len(key)] for i in range(len(data))]

print(("".join(str(i) + " " for i in xor(flag.encode(), key))))

