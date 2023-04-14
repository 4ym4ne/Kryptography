en_letter_freq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51,
               'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09,
               'R': 5.99, 'L': 4.25, 'D': 4.03, 'C': 2.76,
               'U': 2.78, 'M': 2.41, 'W': 2.23, 'F': 2.02,
               'G': 2.36, 'Y': 2.02, 'P': 1.93, 'B': 1.49,
               'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
               'Q': 0.09, 'Z': 0.07}

char_list = [chr(char) for char in range(ord('A'), ord('Z')+1)]
key = list("GOEPNXCVFJSHRZDITWALKUQBMY")

with open('chiffrat.txt', 'r') as f:
    chiffrat = list(f.read())

# Absolute Häufigkeit
def calculate_a_frequency():
    frequency = {}
    for charToCompare in chiffrat:
        if charToCompare in char_list:
            if charToCompare in frequency:
                frequency[charToCompare] += 1
            else:
                frequency[charToCompare] = 1
    return frequency

# Relative Häufigkeit
def calculate_r_frequency(mylist):
    total = sum(mylist.values())
    frequency = {}
    for char in mylist:
        frequency[char] = round((mylist[char] / total) * 100, 2)
    #return sort_list(frequency, order=1)
    return dict(sorted(frequency.items()))


def sort_list(dictionary, order):
    return {k: v for k, v in sorted(dictionary.items(), key=lambda x: -x[order])}


def decrypt(toDecrypt):
    decrypted_output = ""
    #letter_mapping = {key1: key2 for key1, key2 in zip(letter_, en_letter_freq.keys())}
    letter_mapping = {key1: key2 for key1, key2 in zip(char_list, key)}
    print(letter_mapping)

    for char in toDecrypt:
        if char in char_list:
            decrypted_output += letter_mapping[char]
        else:
            decrypted_output += char
    return decrypted_output


list = calculate_a_frequency()
list2 = calculate_r_frequency(list)

print(list2)
print(en_letter_freq)



print("\n==============================================\n")

print(decrypt(chiffrat))
#print(decrypt(chiffrat, list2))
