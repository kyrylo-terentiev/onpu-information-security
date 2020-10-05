import binascii

"""
Created on Tue Sep 24 02:41:32 2020
@author: Kyrylo Terentiev
"""


def encrypt(key, message):
    """ Encryption of the message by given key using Vernam algorithm
        (Bitwise XOR). """
    # convert message and key to its binary representations
    message = convert_str_to_bin(message)
    key = convert_str_to_bin(key)
    key = adopt_key_to_message(key, message)
    print(f'Message (bin) \t\t\t: {message}')
    print(f'Key (bin) \t\t\t\t: {key}')

    encrypted_message = ""
    index = 0
    for char in message:
        # bitwise XOR operation, appending its casted to char result to encoded string
        encrypted_message = encrypted_message + str(int(char) ^ int(key[index]))
        index = index + 1

    return encrypted_message


def decrypt(key, message):
    """ Decryption of encreypted message by given key using Vernam algorithm
        (Bitwise XOR). """
    # convert key to its binary representation
    key = convert_str_to_bin(key)
    key = adopt_key_to_message(key, message)

    decrypted_message = ""
    index = 0
    for char in message:
        # bitwise XOR operation, appending its casted to char result to encoded string
        decrypted_message = decrypted_message + str(int(char) ^ int(key[index]))
        index = index + 1

    print(f'Decrypted message (bin) : {decrypted_message}')
    return convert_bin_to_str(decrypted_message)


def convert_str_to_bin(string):
    """ Conversion of string to its binary representation without leading '0b'. """
    return bin(int(binascii.hexlify(string.encode()), 16))[2:]


def convert_bin_to_str(bin_string):
    """ Decoding of string's binary representation to it's actual value according to default charset. """
    return binascii.unhexlify('%x' % int('0b' + bin_string, 2)).decode()


def adopt_key_to_message(key, message):
    """ Adds extra characters to end of key from it's beginning until len(key) <> len(message) """
    new_key = ""
    i = 0
    while len(new_key) != len(message):
        new_key = new_key + key[i % len(key)]
        i = i + 1

    return new_key


def main():
    print("--- This program performs encryption and decryption of the plaintext using Vernam cipher algorithm ---")
    message = input("Enter the message \t\t: ")
    key = input("Enter the key \t\t\t: ")

    encrypted_message = encrypt(key, message)
    print(f'Encrypted message \t\t: {encrypted_message}')
    decrypted_message = decrypt(key, encrypted_message)
    print(f'Decrypted message \t\t: {decrypted_message}')


if __name__ == "__main__":
    main()
