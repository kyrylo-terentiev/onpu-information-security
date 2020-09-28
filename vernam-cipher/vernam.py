"""
Created on Thu Sep 24 02:44:06 2020
@author: Kyrylo Terentiev
@author: Alex Gerega
"""

error_msg = "Error: Length of Key Must be >= Length of Plaintext"
abc = "abcdefghijklmnopqrstuvwxyz"
mapping_dict = {}


def main():
    print("--- This program performs encryption and decryption of the plaintext using Vernam cipher algorithm ---")
    plain_text = input("Enter the plain text >>> ")
    key = input("Enter the key (key length >= plaintext length) >>> ")
    print()

    if len(key) < len(plain_text):
        raise ValueError(error_msg)

    for abc_letter in abc.upper():
        mapping_dict[abc_letter] = ord(abc_letter) - 65

    plain_text = plain_text.upper()
    key = key.upper()

    cipher_text = vernam_encryption(plain_text, key)

    plain_text = vernam_decryption(cipher_text, key)

    print()
    print("Encrypted cipher text >>> ", cipher_text)
    print("Decrypted plain text >>> ", plain_text)
    print()


def vernam_encryption(plaintext, key):
    """Encryption of plaintext using Vernam cipher algorithm"""
    cipher_text = ''

    for i in range(len(plaintext)):
        plaintext_letter = plaintext[i]
        key_letter = key[i]
        sum = mapping_dict[plaintext_letter] + mapping_dict[key_letter]

        if sum >= 26:
            sum -= 26

        cipher_text += chr(sum + 65)

    return cipher_text


def vernam_decryption(ciphertext, key):
    """Decryption of ciphertext using Vernam cipher algorithm"""
    plain_text = ''

    for i in range(len(ciphertext)):
        cipher_text_letter = ciphertext[i]
        key_letter = key[i]

        diff = mapping_dict[cipher_text_letter] - mapping_dict[key_letter]

        if diff < 0:
            diff += 26

        plain_text += chr(diff + 65)

    return plain_text


if __name__ == "__main__":
    main()