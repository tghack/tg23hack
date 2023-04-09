with open("output.txt", "r") as f:
    data = [int(i) for i in f.read().strip().split(" ")]

for i in range(0x0000, 0xffff):
    key = i.to_bytes(2)
    flag = "".join(chr(data[j] ^ key[j % len(key)]) for j in range(len(data)))
    if flag[0:5] == "TG23{":
        print(flag)
        break


