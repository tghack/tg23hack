import random
import base64
import hashlib

def main():
    user_input = input("Vennligst oppgi den hemmelige koden: ")

    if len(user_input) < 5:
        print("Den hemmelige koden maa ha en lengde paa 5 eller mer. Prov igjen")
        exit()

    random_number = random_generator()
    scrambled = shuffle(random_number, user_input)
    coded = encoder(scrambled)
    get_flag(coded)

def random_generator():
    secret = [""] * 20
    
    for i in range(20):
        for j in range(4, 22, 1):
            secret[i] = i%j

    return secret[random.randint(0, 19)]

def shuffle(key, value):
    scramble = [""] * len(value)

    for p in range(0, key):
        for q in range(p, len(value), key):
            scramble[q] = value[q]
            p += 1

    return ''.join(scramble)

def encoder(plaintext):
    coded = base64.b64encode(plaintext.encode())
    hashed = hashlib.md5(coded)
    encoded = base64.b32encode((hashed.hexdigest()).encode())
    return encoded.decode()

def get_the_good_stuff(): return "VEcyM3szNHMxM3JfdGg0bl8xdF9sMDBrc30="

def decoder(ciphertext, key):
    decode_part1 = base64.b64decode(ciphertext, key)
    decode_part2 = base64.b16encode(decode_part1)
    decode_part3 = hashlib.md5(decode_part2)
    decode_part4 = base64.b32hexdecode(decode_part3)
    decode_part5 = base64.b85decode(decode_part4)
    decode_part6 = base64.b32decode(decode_part5)
    return decode_part6.decode()

def get_flag(user_input):
    random_string = ""
    decoy1 = "SpbBIhb1blItZU"
    decoy2 = "2lXlGlWlGnGvG="
    i = j = 0

    while i < len(decoy1) and j < len(decoy2):
        random_string += decoy1[i] + decoy2[j]
        i +=1
        j+=1

    hashed = hashlib.md5(random_string.encode())
    encoded_string = (base64.b32encode((hashed.hexdigest()).encode())).decode()

    if(encoded_string == user_input):
        print(f"Hurra, du fikk det til! Her er flagget: {(base64.b64decode(get_the_good_stuff())).decode()}")
    else:
        print("Feil kode. Prov igjen")


if __name__ == "__main__":
    main()  