german_freq = {'E': 16.11, 'N': 10.33, 'I': 9.05, 'R': 6.72, 'T': 6.34, 'S': 6.23, 'A': 5.60,
               'H': 5.20, 'D': 4.17, 'U': 3.70, 'C': 3.40, 'L': 3.24, 'G': 2.94, 'M': 2.80,
               'O': 2.32, 'B': 2.19, 'F': 1.71, 'W': 1.39, 'Z': 1.36, 'K': 1.33, 'V': 0.92,
               'P': 0.84, 'J': 0.19, 'X': 0.11, 'Q': 0.07, 'Y': 0.06}

english_freq =    {'E': 13.0, 'T': 9.10, 'A': 8.2, 'O': 7.5, 'I': 6.97, 'N': 6.75, 'S': 6.33,
                  'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.76, 'U': 2.78, 'M': 2.4,
                  'W': 2.4, 'F': 2.02, 'G': 2.36, 'Y': 2.02, 'P': 1.93, 'B': 1.49, 'V': 0.98,
                  'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.09, 'Z': 0.07}

ALPHABET = [chr(char) for char in range(ord('A'), ord('Z') + 1)]


class Decrypter:
    key = list("GOEPNXCVFJSHRZDITWALKUQBMY")

    # Standard index of coincidence for german.
    GERMAN_IC = 0.076
    ENGLISH_IC = 0.06

    def __init__(self, path):
        with open(path, 'r') as f:
            self.chiffrat = f.read()
        self.version = self.chiffrat

    def get_english_frequency(self):
        return english_freq

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
            if char in ALPHABET:
                frequency[char] = round((a_frequency[char] / total)*100, 2)

        return dict(sorted(frequency.items(), key=lambda x: -x[1]))
        #return dict(sorted(frequency))

    def guess_key(self):
        letter_freq = self.calculate_r_frequency(self.chiffrat)
        print(letter_freq)
        print(english_freq)

        mapping = {}
        my_list = list(english_freq.keys())

        for i, key in enumerate(letter_freq):
            # mapping each letter in a dic
            if 1 < i < len(letter_freq)-2:
                mapping[key] = {my_list[i-2], my_list[i-1], my_list[i], my_list[i+1], my_list[i+2]}
            elif i <= 1:
                mapping[key] = {my_list[i]}
            elif i == len(letter_freq)-1:
                mapping[key] = {my_list[i - 4], my_list[i - 3], my_list[i -2], my_list[i - 1], my_list[i]}
            elif i == len(letter_freq)-2:
                mapping[key] = {my_list[i - 3], my_list[i - 2], my_list[i -1], my_list[i], my_list[i+1]}


        # print the keys
        dicta = dict(sorted(mapping.items()))
        print(dicta)


    def get_bigrams(self):
        bigrams = {}
        for i in range(len(self.chiffrat) - 1):

            curr_big = self.chiffrat[i:i+2]
            if curr_big.isalpha():
                if curr_big in bigrams:
                    bigrams[curr_big] += 1
                else:
                    bigrams[curr_big] = 1

        return dict(sorted(bigrams.items(), key=lambda x: -x[1]))

    def print_by_letter_freq(self):
        res = self.chiffrat
        for k, v in zip(self.calculate_r_frequency(self.chiffrat), english_freq):
            res = res.replace(k, v)
        return res

    def print_version(self, before, after):
        version = self.version.replace(before, after)
        print(version)

    def decrypt_sub(self, toDecrypt, key):
        decrypted_output = ""
        # letter_mapping = {key1: key2 for key1, key2 in zip(letter_, en_letter_freq.keys())}
        letter_mapping = {key1: key2 for key1, key2 in zip(ALPHABET, key)}
        print(letter_mapping)

        for char in toDecrypt:
            if char in ALPHABET:
                decrypted_output += letter_mapping[char]
            else:
                decrypted_output += char
        return decrypted_output

    #############################################################

    def calculate_ic(self, text):
        cipher_len = len(text)
        freqs = self.calculate_a_frequency(text)
        freqsum = 0.0

        for letter in ALPHABET:
            freqsum += freqs[letter] * (freqs[letter] - 1)

        return freqsum / (cipher_len * (cipher_len - 1))


    def find_key_length(self):
        for key_range in range(2, 20):
            sum = 0

            for cut_from in range(0, key_range):
                # cut it to substring
                substring = self.chiffrat[cut_from:len(self.chiffrat):key_range]
                # Summe der gesamsten IC der substring

                sum += self.calculate_ic(substring)

            print("length ", key_range, " # I.C: ", sum / (cut_from + 1))

            if sum/(cut_from+1) >= 0.07:
                key_length = key_range
                print("LENGTH OF THE KEY IS ", key_length)
                return key_length



    def shift(self, text, i):
        shifted = ''
        for letter in text:
            shifted += ALPHABET[(ALPHABET.index(letter) - i) % len(ALPHABET)]
        return shifted

    def _corr(self, text, lfreq):
        return sum([(lfreq[letter] * german_freq[letter]) for letter in text])

    def _find_key_letter(self, text, lfreq):
        key_letter = ''
        max_corr = 00
        for count, letter in enumerate(ALPHABET):
            shifted = self.shift(text=text, i=count)
            corr = self._corr(text=shifted, lfreq=lfreq)
            print(shifted, " ===> ", corr)
            if corr > max_corr:
                max_corr = corr
                key_letter = letter
        print("Key: ", key_letter, "Max  ===> ", max_corr)

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
        columns = []
        for letter_c in range(len(blocks[0])):
            column = ''
            for group_c in range(len(blocks)):
                column += blocks[group_c][letter_c]
            columns.append(column)
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
    decrypter = Decrypter("chiffrat.txt")
    print(decrypter.guess_key())
    #print(decrypter.print_by_letter_freq())

    #print(decrypter.get_bigrams())

    #decrypter.print_version("PE", "TH")

    #print(decrypter.find_key_length())
    #assert decrypter.restore_key(decrypter.chiffrat, 10) == "FWQGCZXUGP", "Should be FWQGCZXUGP"
    #print(decrypter.restore_key(decrypter.chiffrat, 10))
    #print(decrypter.vigenere_decode(decrypter.chiffrat, "FWQGCZXUGP"))
    # print(decrypter.decrypt_sub(decrypter.chiffrat))
