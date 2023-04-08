char_list = [chr(char) for char in range(ord('A'), ord('Z')+1)]
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
    return frequency


list = calculate_a_frequency()
print(list)
print(calculate_r_frequency(list))