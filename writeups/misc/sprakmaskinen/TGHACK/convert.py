
with open('orginal_text.txt') as fh:
    sentence = fh.readlines()[0]

binary = (' '.join('{0:08b}'.format(ord(l),'b') for l in sentence)).split(' ')
encoded = []

for letter in binary:
    rev = letter[::-1]
    logical_occurence = [str(i+1) for i, val in enumerate(rev) if val == '1']
    res = ''.join(logical_occurence)
    encoded.append(res)

print(' '.join(encoded))

'''
8-bit
87654321
'''
