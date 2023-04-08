import string

#german_freq = [16.11, 10.33, 9.05, 6.72, 6.34, 6.23, 5.6, 5.2, 4.17, 3.7, 3.4, 3.24, 2.94, 2.8,
#               2.32, 2.19, 1.71, 1.39, 1.36, 1.33, 0.92, 0.84, 0.64, 0.51, 0.36, 0.19, 0.19, 0.11, 0.07, 0.06]
german_freq = {'E': 16.11, 'N': 10.33, 'I': 9.05, 'R': 6.72, 'T': 6.34, 'S': 6.23, 'A': 5.60,
               'H': 5.20, 'D': 4.17, 'U': 3.70, 'C': 3.40, 'L': 3.24, 'G': 2.94, 'M': 2.80,
               'O': 2.32, 'B': 2.19, 'F': 1.71, 'W': 1.39, 'Z': 1.36, 'K': 1.33, 'V': 0.92,
               'P': 0.84, 'J': 0.19, 'X': 0.11, 'Q': 0.07, 'Y': 0.06}

AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
cipherKey = "FWQGCZXUGP"
AZL = len(AZ)  # Length of Alphabet

class Decrypter:

    char_list = [chr(char) for char in range(ord('A'), ord('Z') + 1)]
    key = list("GOEPNXCVFJSHRZDITWALKUQBMY")

    # Standard index of coincidence for English.
    ENGLISH_IC = 0.076

    def __init__(self, path):
        with open(path, 'r') as f:
            self.chiffrat = f.read()

    def calculate_a_frequency(self, text):
        frequency = {letter: 0 for letter in self.char_list}
        for charToCompare in text:
            if charToCompare in frequency:
                frequency[charToCompare] += 1
        return frequency

    def calculate_r_frequency(self, text):
        a_frequency = self.calculate_a_frequency(text)
        total = sum(a_frequency.values())
        frequency = {}
        for char in text:
            frequency[char] = (a_frequency[char] / total)
        #return self.sort_list(frequency, order=1)
        return dict(sorted(frequency.items()))

    def sort_list(self, dictionary, order):
        return {k: v for k, v in sorted(dictionary.items(), key=lambda x: -x[order])}

    def decrypt_sub(self, toDecrypt):
        decrypted_output = ""
        # letter_mapping = {key1: key2 for key1, key2 in zip(letter_, en_letter_freq.keys())}
        letter_mapping = {key1: key2 for key1, key2 in zip(self.char_list, self.key)}
        print(letter_mapping)

        before = str(toDecrypt).split("\n")
        for char in toDecrypt:
            if char in self.char_list:
                decrypted_output += letter_mapping[char]
            else:
                decrypted_output += char
        return decrypted_output

    def calculate_ic(self, text):
        cipher_len = len(text)
        freqs = self.calculate_a_frequency(text)
        freqsum = 0.0

        for letter in self.char_list:
            freqsum += freqs[letter] * (freqs[letter] - 1)

        return freqsum / (cipher_len * (cipher_len - 1))

    def find_key_length(self, chiffrat):
        for i in range(2, 20):
            sum = 0

            for j in range(0, i):
                # cut it to substring
                substring = chiffrat[j:len(chiffrat):i]
                # Summe der gesamsten IC der substring
                sum += self.calculate_ic(substring)


            print("length ", i, "I.C: ", sum / (j + 1))
            if (sum / (j + 1) >= 0.06):
                key_length = i
                print("LENGTH OF THE KEY IS ", key_length)
                return key_length

    #################################################

    def shift(self, text, amount):
        shifted = ''
        for letter in text:
            shifted += self.char_list[(self.char_list.index(letter) - amount) % len(self.char_list)]
        return shifted

    def _corr(self, text, lfreq):
        return sum([(lfreq[letter] * german_freq[letter]) for letter in text])

    def _find_key_letter(self, text, lfreq):
        key_letter = ''
        max_corr = 00
        for count, letter in enumerate(string.ascii_uppercase):
            shifted = self.shift(text=text, amount=count)
            #print(shifted)
            corr = self._corr(text=shifted, lfreq=lfreq)
            #print(corr)
            if corr > max_corr:
                max_corr = corr
                key_letter = letter
        return key_letter

    def restore_key(self, cyphertext, key_len):
        key = ''
        vektors = self.get_vektor(text=cyphertext, size=key_len)
        frequencies = self.calculate_r_frequency(cyphertext)

        for vektor in vektors:
            key += self._find_key_letter(text=vektor, lfreq=frequencies)
        return key


    def get_vektor(self, text, size):
        blocks = [text[i:i + size] for i in range(0, len(text) - size, size)]
        group_size = len(blocks[0])
        columns = []
        for letter_count in range(group_size):
            column = ''
            for group_count in range(len(blocks)):
                column += blocks[group_count][letter_count]
            columns.append(column)
        print(columns)
        return columns

    def vigenere_decode(self, ciphertext, key):
        """Decode a Vigenere cipher using a given key."""
        plaintext = ""
        key_index = 0
        for c in ciphertext:
            if c not in self.char_list:
                plaintext += c
                continue
            c_index = self.char_list.index(c)
            k_index = self.char_list.index(key[key_index])
            p_index = (c_index - k_index) % 26

            plaintext += self.char_list[p_index]
            key_index = (key_index + 1) % len(key)

        return plaintext

if __name__ == '__main__':
    decrypter = Decrypter("chiffrat2.txt")
    print(decrypter.restore_key(decrypter.chiffrat, 10))
    #print(decrypter.get_text_matrix(decrypter.chiffrat))
    print(decrypter.vigenere_decode(decrypter.chiffrat, "FWQGCZXUGP"))

    #print(decrypter.decrypt_sub(decrypter.chiffrat))