from matplotlib import pyplot as plt

"""
Created on Thu Oct 1 22:43:23 2020
@author: Kyrylo Terentiev
@author: Alex Gerega
"""

block_size = 8
bit_block_size = 64
rounds = 8
files_path = "files/"


def main():
    print("--- This program performs encryption and decryption of the plaintext using Feistel cipher algorithm ---")

    open_text_filename = "opentext.txt"
    key_filename = "key.txt"
    encrypted_filename = "encrypted.txt"

    with open(files_path + open_text_filename, "r") as f:
        input = f.read()
        print("Enter text to encrypt >>> " + input)

    with open(files_path + key_filename, "r") as f:
        key = f.read()
        print("Ecnryption key >>> " + key)

    encrypted, bit_num, key_bit_num = encrypt(key, input)
    print("Encrypted message >>> " + encrypted)
    decrypted = decrypt(key, encrypted)
    print("Decrypted message >>> " + decrypted)

    print("Number of changed bits according in message >>> " + str(bit_num))
    print("Number of changed bits according in key >>> " + str(key_bit_num))

    plt.plot(bit_num, label='Message change')
    plt.plot(key_bit_num, label='Key change')
    plt.legend()
    plt.show()

    with open(files_path + encrypted_filename, 'w+', encoding="utf-8") as fw:
        fw.write(encrypted)


def encrypt(key, message):
    cipher_text = ""
    n = block_size  # 8 bytes (64 bits) per block

    message = [message[i: i + n] for i in range(0, len(message), n)]

    last_block_length = len(message[len(message) - 1])

    if (last_block_length < block_size):
        for i in range(last_block_length, block_size):
            message[len(message) - 1] += " "

    key_initial = key
    num_bit = []
    num_bit_key = []
    j = 0
    for block in message:

        if j == 0:
            # print(block)
            changed_block = chr(ord(block[0]) - 1) + block[1:]
            # print(changed_block)
            changed_key = chr(ord(key_initial[0]) - 1) + key_initial[1:]
            num_bit.append(count(string_to_bin(changed_block), string_to_bin(block)))
            num_bit_key.append(count(string_to_bin(key_initial), string_to_bin(changed_key)))

        left = [""] * (rounds + 1)
        right = [""] * (rounds + 1)
        left[0] = block[0:block_size // 2]
        right[0] = block[block_size // 2:block_size]

        left_2 = [""] * (rounds + 1)
        right_2 = [""] * (rounds + 1)
        left_2[0] = changed_block[0:block_size // 2]
        right_2[0] = changed_block[block_size // 2:block_size]

        left_3 = [""] * (rounds + 1)
        right_3 = [""] * (rounds + 1)
        left_3[0] = block[0:block_size // 2]
        right_3[0] = block[block_size // 2:block_size]

        for i in range(1, rounds + 1):

            left[i] = right[i - 1]
            key = round_key(key_initial, i)
            right[i] = xor(left[i - 1], xor(right[i - 1], key))

            if j == 0:
                left_2[i] = right_2[i - 1]
                right_2[i] = xor(left_2[i - 1], xor(right_2[i - 1], key))
                # print(count(stobin("".join(L[i]+right[i])), stobin("".join(L2[i]+R2[i]))))
                num_bit.append(count(string_to_bin(block), string_to_bin("".join(left_2[i] + right_2[i]))))

                left_3[i] = right_3[i - 1]
                key = round_key(changed_key, i)
                right_3[i] = xor(left_3[i - 1], xor(right_3[i - 1], key))
                num_bit_key.append(count(string_to_bin(block), string_to_bin("".join(left_3[i] + right_3[i]))))

        cipher_text += (left[rounds] + right[rounds])

        j = j + 1

    return cipher_text, num_bit, num_bit_key


def count(str1, str2):
    count = 0
    for s1, s2 in zip(str1, str2):
        if s1 != s2:
            count = count + 1
    return count


def decrypt(key, cipher_text):
    message = ""
    n = block_size  # 8 bytes (64 bits) per block

    cipher_text = [cipher_text[i: i + n] for i in range(0, len(cipher_text), n)]

    last_block_length = len(cipher_text[len(cipher_text) - 1])

    if (last_block_length < block_size):
        for i in range(last_block_length, block_size):
            cipher_text[len(cipher_text) - 1] += " "

    key_initial = key
    for block in cipher_text:
        L = [""] * (rounds + 1)
        R = [""] * (rounds + 1)
        L[rounds] = block[0:block_size // 2]
        R[rounds] = block[block_size // 2:block_size]

        for i in range(rounds, 0, -1):
            key = round_key(key_initial, i)
            R[i - 1] = L[i]
            L[i - 1] = xor(R[i], xor(L[i], key))

        message += (L[0] + R[0])

    return message


def round_key(key, i):
    return (key[i:i + block_size])


def xor(s1, s2):
    """xor two strings"""
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))


def string_to_bin(s):
    """string to binary"""
    return ''.join('{:08b}'.format(ord(c)) for c in s)


def bit_to_int(s):
    """binary to int"""
    return int(s, 2)


def int_to_bin(i):
    """int to binary"""
    return bin(i)


def toggle_bit(int_type, offset):
    mask = 1 << offset
    return (int_type ^ mask)


def bin_to_string(b):
    """binary to string"""
    return ''.join(chr(int(b[i: i + 8], 2)) for i in range(0, len(b), 8))


if __name__ == "__main__":
    main()