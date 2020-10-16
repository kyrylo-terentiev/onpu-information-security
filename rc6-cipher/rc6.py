"""
Created on Thu Oct 15 01:13:45 2020
@author: Kyrylo Terentiev
@author: Alex Gerega
"""

PATH_TO_FILES = "data/"


# rotate right input x, by n bits
def rotate_right(x, n, bits=32):
    mask = (2 ** n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (bits - n))


# rotate left input x, by n bits
def rotate_left(x, n, bits=32):
    return rotate_right(x, bits - n, bits)


# convert input sentence into blocks of binary
# creates 4 blocks of binary each of 32 bits.
def convert_str_to_blocks(sentence):
    encoded = []
    res = ""
    for i in range(0, len(sentence)):
        if i % 4 == 0 and i != 0:
            encoded.append(res)
            res = ""
        temp = bin(ord(sentence[i]))[2:]
        if len(temp) < 8:
            temp = "0" * (8 - len(temp)) + temp
        res = res + temp
    encoded.append(res)
    return encoded


# converts 4 blocks array of long int into string
def convert_blocks_to_str(blocks):
    s = ""
    for block in blocks:
        temp = bin(block)[2:]
        if len(temp) < 32:
            temp = "0" * (32 - len(temp)) + temp
        for i in range(0, 4):
            s = s + chr(int(temp[i * 8:(i + 1) * 8], 2))
    return s


# generate key s[0... 2r+3] from given input string userkey
def generate_key(user_key):
    r = 12
    w = 32
    b = len(user_key)
    modulo = 2 ** 32
    s = (2 * r + 4) * [0]
    s[0] = 0xB7E15163
    for i in range(1, 2 * r + 4):
        s[i] = (s[i - 1] + 0x9E3779B9) % (2 ** w)
    encoded = convert_str_to_blocks(user_key)
    # print encoded
    encoded_len = len(encoded)
    l = encoded_len * [0]
    for i in range(1, encoded_len + 1):
        l[encoded_len - i] = int(encoded[i - 1], 2)

    v = 3 * max(encoded_len, 2 * r + 4)
    A = B = i = j = 0

    for index in range(0, v):
        A = s[i] = rotate_left((s[i] + A + B) % modulo, 3, 32)
        B = l[j] = rotate_left((l[j] + A + B) % modulo, (A + B) % 32, 32)
        i = (i + 1) % (2 * r + 4)
        j = (j + 1) % encoded_len
    return s


# encryption using RC6 algorithm
def encrypt(message, s):
    encoded = convert_str_to_blocks(message)
    A = int(encoded[0], 2)
    B = int(encoded[1], 2)
    C = int(encoded[2], 2)
    D = int(encoded[3], 2)
    org_i = []
    org_i.append(A)
    org_i.append(B)
    org_i.append(C)
    org_i.append(D)
    r = 12
    w = 32
    modulo = 2 ** 32
    lgw = 5
    B = (B + s[0]) % modulo
    D = (D + s[1]) % modulo
    for i in range(1, r + 1):
        t_temp = (B * (2 * B + 1)) % modulo
        t = rotate_left(t_temp, lgw, 32)
        u_temp = (D * (2 * D + 1)) % modulo
        u = rotate_left(u_temp, lgw, 32)
        tmod = t % 32
        umod = u % 32
        A = (rotate_left(A ^ t, umod, 32) + s[2 * i]) % modulo
        C = (rotate_left(C ^ u, tmod, 32) + s[2 * i + 1]) % modulo
        (A, B, C, D) = (B, C, D, A)
    A = (A + s[2 * r + 2]) % modulo
    C = (C + s[2 * r + 3]) % modulo
    cipher = []
    cipher.append(A)
    cipher.append(B)
    cipher.append(C)
    cipher.append(D)
    return org_i, cipher


# decryption using RC6 algorithm
def decrypt(message, s):
    encoded = convert_str_to_blocks(message)
    A = int(encoded[0], 2)
    B = int(encoded[1], 2)
    C = int(encoded[2], 2)
    D = int(encoded[3], 2)
    cipher = []
    cipher.append(A)
    cipher.append(B)
    cipher.append(C)
    cipher.append(D)
    r = 12
    w = 32
    modulo = 2 ** 32
    lgw = 5
    C = (C - s[2 * r + 3]) % modulo
    A = (A - s[2 * r + 2]) % modulo
    for j in range(1, r + 1):
        i = r + 1 - j
        (A, B, C, D) = (D, A, B, C)
        u_temp = (D * (2 * D + 1)) % modulo
        u = rotate_left(u_temp, lgw, 32)
        t_temp = (B * (2 * B + 1)) % modulo
        t = rotate_left(t_temp, lgw, 32)
        tmod = t % 32
        umod = u % 32
        C = (rotate_right((C - s[2 * i + 1]) % modulo, tmod, 32) ^ u)
        A = (rotate_right((A - s[2 * i]) % modulo, umod, 32) ^ t)
    D = (D - s[1]) % modulo
    B = (B - s[0]) % modulo
    org_i = []
    org_i.append(A)
    org_i.append(B)
    org_i.append(C)
    org_i.append(D)
    return cipher, org_i


def main():
    print("------------------------------------------------------------------------------------------------")
    print("--- This program performs encryption and decryption using RC6 cipher algorithm (Bitwise) ---")
    print("------------------------------------------------------------------------------------------------")
    print("Update key and open text in 'data/' directory.")
    open_text_filename = "./open_text.txt"
    key_filename = "./key.txt"
    encrypted_filename = "./encrypted.txt"

    with open(PATH_TO_FILES + open_text_filename, "r") as f:
        message = f.read()
        print("Message to encrypt: " + message)

    with open(PATH_TO_FILES + key_filename, "r") as f:
        key = f.read()
        print("Key: " + key)

    s = generate_key(key)
    n = 16

    sentence = [message[i: i + n] for i in range(0, len(message), n)]

    last_block_len = len(sentence[len(sentence) - 1])

    if last_block_len < n:
        for i in range(last_block_len, n):
            sentence[len(sentence) - 1] += " "

    encrypted = ""
    encrypted_arr = []

    for block in sentence:
        org_i, cipher = encrypt(block, s)
        sentence = convert_blocks_to_str(cipher)
        encrypted = encrypted + sentence
        encrypted_arr.append(cipher)

    print("\nEncrypted string array: ", encrypted_arr)
    print("\nEncrypted string: " + encrypted)
    print("Length of encrypted string: ", len(encrypted))

    with open(PATH_TO_FILES + encrypted_filename, 'w+', encoding="utf-8") as fw:
        fw.write(encrypted)

    encrypted = [encrypted[i: i + n] for i in range(0, len(encrypted), n)]

    decrypted = ""
    decrypted_list = []

    for block in encrypted:
        cipher, org_i = decrypt(block, s)
        sentence = convert_blocks_to_str(org_i)
        decrypted = decrypted + sentence
        decrypted_list.append(org_i)

    print("\nDecrypted string array: ", decrypted_list)
    print("Decrypted string: " + decrypted)
    print("Length of decrypted string: ", len(decrypted))


if __name__ == "__main__":
    main()
