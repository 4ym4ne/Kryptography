german_freq = {'E': 16.11, 'N': 10.33, 'I': 9.05, 'R': 6.72, 'T': 6.34, 'S': 6.23, 'A': 5.60,
               'H': 5.20, 'D': 4.17, 'U': 3.70, 'C': 3.40, 'L': 3.24, 'G': 2.94, 'M': 2.80,
               'O': 2.32, 'B': 2.19, 'F': 1.71, 'W': 1.39, 'Z': 1.36, 'K': 1.33, 'V': 0.92,
               'P': 0.84, 'J': 0.19, 'X': 0.11, 'Q': 0.07, 'Y': 0.06}

ALPHABET = [chr(char) for char in range(ord('A'), ord('Z') + 1)]
cipherKey = "FWQGCZXUGP"




class Decrypter:
    key = list("GOEPNXCVFJSHRZDITWALKUQBMY")

    # Standard index of coincidence for german.
    GERMAN_IC = 0.076

    def __init__(self, path):
        with open(path, 'r') as f:
            self.chiffrat = f.read()

    def calculate_a_frequency(self, text):
        frequency = {letter: 0 for letter in ALPHABET}
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
        # return self.sort_list(frequency, order=1)
        return dict(sorted(frequency.items()))

    def sort_list(self, dictionary, order):
        return {k: v for k, v in sorted(dictionary.items(), key=lambda x: -x[order])}

    def decrypt_sub(self, toDecrypt):
        decrypted_output = ""
        # letter_mapping = {key1: key2 for key1, key2 in zip(letter_, en_letter_freq.keys())}
        letter_mapping = {key1: key2 for key1, key2 in zip(ALPHABET, self.key)}
        print(letter_mapping)

        before = str(toDecrypt).split("\n")
        for char in toDecrypt:
            if char in ALPHABET:
                decrypted_output += letter_mapping[char]
            else:
                decrypted_output += char
        return decrypted_output

    def calculate_ic(self, text):
        cipher_len = len(text)
        freqs = self.calculate_a_frequency(text)
        freqsum = 0.0

        for letter in ALPHABET:
            freqsum += freqs[letter] * (freqs[letter] - 1)

        return freqsum / (cipher_len * (cipher_len - 1))

    def find_key_length(self, chiffrat):
        for key_range in range(2, 20):
            sum = 0

            for cut_from in range(0, key_range):
                # cut it to substring
                substring = chiffrat[cut_from:len(chiffrat):key_range]
                # Summe der gesamsten IC der substring
                sum += self.calculate_ic(substring)

            print("length ", key_range, "I.C: ", sum / (cut_from + 1))

            if sum/(cut_from+1) >= 0.06:
                key_length = key_range
                print("LENGTH OF THE KEY IS ", key_length)
                return key_length

    #################################################

    def shift(self, text, amount):
        shifted = ''
        for letter in text:
            shifted += ALPHABET[(ALPHABET.index(letter) - amount) % len(ALPHABET)]
        return shifted

    def _corr(self, text, lfreq):
        return sum([(lfreq[letter] * german_freq[letter]) for letter in text])

    def _find_key_letter(self, text, lfreq):
        key_letter = ''
        max_corr = 00
        for count, letter in enumerate(ALPHABET):
            shifted = self.shift(text=text, amount=count)
            # print(shifted)
            corr = self._corr(text=shifted, lfreq=lfreq)
            # print(corr)
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
        " get the Vektor from the text blocks"
        blocks = [text[i:i + size] for i in range(0, len(text) - size, size)]
        group_size = len(blocks[0])
        columns = []
        for letter_count in range(group_size):
            column = ''
            for group_count in range(len(blocks)):
                column += blocks[group_count][letter_count]
            columns.append(column)
        #print(columns)
        return columns

    def vigenere_decode(self, chiffrat, key):
        """Decode a Vigenere cipher using a given key."""
        plaintext = ""
        key_index = 0
        for c in chiffrat:
            c_index = ALPHABET.index(c)
            k_index = ALPHABET.index(key[key_index])
            p_index = (c_index - k_index) % 26

            plaintext += ALPHABET[p_index]
            key_index = (key_index + 1) % len(key)

        return plaintext


if __name__ == '__main__':
    decrypter = Decrypter("chiffrat2.txt")
    assert decrypter.restore_key(decrypter.chiffrat, 10) == "FWQGCZXUGP", "Should be FWQGCZXUGP"
    # print(decrypter.restore_key(decrypter.chiffrat, 10))
    # print(decrypter.get_text_matrix(decrypter.chiffrat))
    # print(decrypter.vigenere_decode(decrypter.chiffrat, "FWQGCZXUGP"))

    # print(decrypter.decrypt_sub(decrypter.chiffrat))
