
with open('Uploads/sprakmaskin.txt') as fh:
    encoded = fh.readlines()[0].split(' ')

for entry in encoded:
    writeable_bits = ['0','0','0','0','0','0','0','0']
    for numb in entry:
        true_index = int(numb) - 1
        writeable_bits[true_index] = '1'
    bits = (''.join(writeable_bits))[::-1]
    print(int(bits,2).to_bytes(8,'big').decode('latin-1'), end='')