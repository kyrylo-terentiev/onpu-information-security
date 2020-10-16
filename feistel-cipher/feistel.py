import binascii
import matplotlib.pyplot as plt
import numpy as np

"""
Created on Thu Oct 9 12:09:23 2020
@author: Kyrylo Terentiev
@author: Alex Gerega
"""

# store open text here
PATH_TO_OPEN_TEXT_FILE = "data/opentext.txt"
# store encryption key here
PATH_TO_KEY_FILE = "data/key.txt"
# encrypted text is stored here
PATH_TO_ENCRYPTED_FILE = "data/encrypted.txt"
# decrypted text is stored here
PATH_TO_DECRYPTED_FILE = "data/decrypted.txt"
# binary open text is stored here
PATH_TO_BINARY_OPEN_TEXT_FILE = "binary-data/opentext.txt"
# binary key is stored here
PATH_TO_BINARY_KEY_FILE = "binary-data/key.txt"
# binary encrypted text is stored here
PATH_TO_BINARY_ENCRYPTED_FILE = "binary-data/encrypted.txt"

KEY_MODE_EXCEPTION = "Unsupported key mode!"
FUNCTION_MODE_EXCEPTION = "Unsupported function mode!"

SCRAMBLING_RANK_8 = "000000011"
SCRAMBLING_RANK_16 = "0100000000000011"
BITS_TO_SCRAMBLE = 8
ROUNDS = 8

is_open_text_normalized = False
normalization_zeros = "00000000"


def text_to_bits(text):
    return ''.join('{:08b}'.format(ord(char)) for char in text)


def text_from_bits(bits):
    return ''.join(chr(int(bits[i: i + 8], 2)) for i in range(0, len(bits), 8))


def int_to_bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def circular_bit_shift(bit_str, round_num):
    bits_arr = list(bit_str)
    shifted_bits_arr = []

    i = round_num

    for step in range(0, len(bits_arr)):
        if i >= len(bits_arr):
            i = 0
        shifted_bits_arr.append(bits_arr[i])
        i += 1

    return ''.join([str(char) for char in shifted_bits_arr])


def scramble_bit(bit_str, round_num):
    bits_circle = list(circular_bit_shift(bit_str, round_num))

    rank_circled = ''
    for i in range(0, BITS_TO_SCRAMBLE):
        rank_circled += bits_circle[i]

    scrambled = rank_circled
    scrambler = SCRAMBLING_RANK_8
    scramble_result = exor(scrambled, scrambler)
    return normalization_zeros + scramble_result


def exor(a, b):
    temp = ""

    for i in range(len(a)):

        if a[i] == b[i]:
            temp += "0"

        else:
            temp += "1"

    return temp


def get_changed_bits_count(prev_rl, new_rl):
    prev_rl_arr = list(prev_rl)
    new_rl_arr = list(new_rl)
    changed_bits_num = 0
    for bit in range(0, len(new_rl_arr)):
        if new_rl_arr[bit] != prev_rl_arr[bit]:
            changed_bits_num += 1

    return changed_bits_num


def single_function_encode(open_text, key, round_num, is_key_circular):
    left = text_to_bits(open_text[:int(len(open_text) / 2)])
    right = text_to_bits(open_text[int(len(open_text) / 2):])
    bits_changed = []
    for round in range(1, round_num + 1):
        prev_right = right
        prev_left = left

        if is_key_circular:
            result_vi = circular_bit_shift(text_to_bits(key), round)
        else:
            vi = scramble_bit(text_to_bits(key), round)
            zeros_to_add_num = len(prev_left) - len(vi)
            for i in range(0, zeros_to_add_num):
                vi += "0"
            result_vi = vi

        left = exor(prev_right, exor(prev_left, result_vi))
        right = prev_left

        bits_changed.append(get_changed_bits_count(prev_right + prev_left, left + right))

    encoded_file = open(PATH_TO_ENCRYPTED_FILE, "w", encoding='utf-8')
    encoded_file.write(text_from_bits(left) + text_from_bits(right))
    encoded_file.close()

    encoded_file = open(PATH_TO_BINARY_ENCRYPTED_FILE, "w", encoding='utf-8')
    encoded_file.write(left + right)
    encoded_file.close()
    return bits_changed


def single_function_decode(encoded_text, key, round_num, is_key_circular):
    left = text_to_bits(encoded_text[:int(len(encoded_text) / 2)])
    right = text_to_bits(encoded_text[int(len(encoded_text) / 2):])

    vi_arr = []
    for round in range(1, round_num + 1):
        if is_key_circular:
            vi_arr.append(circular_bit_shift(text_to_bits(key), round))
        else:
            vi = scramble_bit(text_to_bits(key), round)
            zeros_to_add_num = len(left) - len(vi)
            for i in range(0, zeros_to_add_num):
                vi += "0"
            vi_arr.append(vi)

    for round in range(round_num, 0, -1):
        vi_index = round - 1
        left_i = exor(right, exor(left, vi_arr[vi_index]))
        left = right
        right = left_i

    if is_open_text_normalized:
        right = right[0:len(right) - len(normalization_zeros)]

    decoded_file = open(PATH_TO_DECRYPTED_FILE, "w", encoding='utf-8')
    decoded_file.write(text_from_bits(left) + text_from_bits(right))
    decoded_file.close()


def complex_function_encode(open_text, key, round_num, is_key_circular):
    left = text_to_bits(open_text[:int(len(open_text) / 2)])
    right = text_to_bits(open_text[int(len(open_text) / 2):])
    bits_changed = []

    for round in range(1, round_num + 1):
        prev_right = right
        prev_left = left

        if is_key_circular:
            vi = circular_bit_shift(text_to_bits(key), round)
            zeros_to_add_num = len(vi) - len(SCRAMBLING_RANK_16)
            temp_scrambling_rank_16 = ""
            for i in range(0, zeros_to_add_num):
                temp_scrambling_rank_16 += "0"
            temp_scrambling_rank_16 += SCRAMBLING_RANK_16
            scrambled_vi = exor(vi, temp_scrambling_rank_16)
        else:
            vi = scramble_bit(text_to_bits(key), round)
            scrambled_vi = exor(vi, SCRAMBLING_RANK_16)
            zeros_to_add_num = len(left) - len(scrambled_vi)
            for i in range(0, zeros_to_add_num):
                scrambled_vi += "0"

        left = exor(prev_right, exor(prev_left, scrambled_vi))
        right = prev_left
        bits_changed.append(get_changed_bits_count(prev_right + prev_left, left + right))

    encoded_file = open(PATH_TO_ENCRYPTED_FILE, "w", encoding='utf-8')
    encoded_file.write(text_from_bits(left) + text_from_bits(right))
    encoded_file.close()

    encoded_file = open(PATH_TO_BINARY_ENCRYPTED_FILE, "w", encoding='utf-8')
    encoded_file.write(left + right)
    encoded_file.close()
    return bits_changed


def complex_function_decode(encoded_text, key, round_num, is_key_circular):
    left = text_to_bits(encoded_text[:int(len(encoded_text) / 2)])
    right = text_to_bits(encoded_text[int(len(encoded_text) / 2):])

    vi_arr = []
    for round in range(1, round_num + 1):
        if is_key_circular:
            vi = circular_bit_shift(text_to_bits(key), round)
            zeros_to_add_num = len(vi) - len(SCRAMBLING_RANK_16)
            temp_scrambling_rank_16 = ""
            for i in range(0, zeros_to_add_num):
                temp_scrambling_rank_16 += "0"
            temp_scrambling_rank_16 += SCRAMBLING_RANK_16
            scrambled_vi = exor(vi, temp_scrambling_rank_16)
            vi_arr.append(scrambled_vi)
        else:
            vi = scramble_bit(text_to_bits(key), round)
            scrambled_vi = exor(vi, SCRAMBLING_RANK_16)
            zeros_to_add_num = len(left) - len(scrambled_vi)
            for i in range(0, zeros_to_add_num):
                scrambled_vi += "0"
            vi_arr.append(scrambled_vi)

    for round in range(round_num, 0, -1):
        vi_index = round - 1
        scrambled_vi = vi_arr[vi_index]
        left_i = exor(right, exor(left, scrambled_vi))
        left = right
        right = left_i

    if is_open_text_normalized:
        right = right[0:len(right) - len(normalization_zeros)]

    decoded_file = open(PATH_TO_DECRYPTED_FILE, "w", encoding='utf-8')
    decoded_file.write(text_from_bits(left) + text_from_bits(right))
    decoded_file.close()


def check_key(key, open_text):
    if len(key) > int(len(open_text) / 2):
        raise Exception("Key length should be half of the open text length!")
    elif len(key) < int(len(open_text) / 2):
        diff = int(len(open_text) / 2) - len(key)
        key = key + text_from_bits("0" * diff)
    return key


def check_open_text(open_text):
    if len(open_text) % 2 != 0:
        global is_open_text_normalized
        is_open_text_normalized = True
        return open_text + text_from_bits(normalization_zeros)
    return open_text


def write_binary_open_text_file(filepath, text):
    encoded_file = open(filepath, "w", encoding='utf-8')
    encoded_file.write(text_to_bits(text))
    encoded_file.close()


def write_binary_key_file(filepath, keyWord):
    encoded_file = open(filepath, "w", encoding='utf-8')
    encoded_file.write(text_to_bits(keyWord))
    encoded_file.close()


def avalanche_effect(bit_to_change_index, is_key_change, path_to_binary_key_file, path_to_binary_open_text_file,
                     is_single_function, is_key_circular):
    # count of bits before avalanche effect
    open_text = text_from_bits(open(path_to_binary_open_text_file, "r").readline())
    key = check_key(text_from_bits(open(path_to_binary_key_file, "r").readline()), open_text)
    if is_single_function:
        bits_changed_before_avalanche_effect = single_function_encode(open_text, key, ROUNDS, is_key_circular)
    else:
        bits_changed_before_avalanche_effect = complex_function_encode(open_text, key, ROUNDS, is_key_circular)

    # change bit on index = bit_to_change_index in key file or open text file
    if is_key_change:
        filepath = path_to_binary_key_file
    else:
        filepath = path_to_binary_open_text_file

    file_to_change = open(filepath, "r+", encoding='utf-8')
    bit_sequence = list(file_to_change.readline())
    file_to_change.truncate(0)

    bit_sequence[bit_to_change_index] = "1" if bit_sequence[bit_to_change_index] == "0" else "0"
    new_bit_sequence = "".join(bit_sequence)
    open(filepath, "w", encoding='utf-8').write(new_bit_sequence)
    # ---------------------------------

    # count bits after avalanche
    open_text = text_from_bits(open(path_to_binary_open_text_file, "r").readline())
    key = check_key(text_from_bits(open(path_to_binary_key_file, "r").readline()), open_text)

    if is_single_function:
        bits_changed_after_avalanche_effect = single_function_encode(open_text, key, ROUNDS, is_key_circular)
    else:
        bits_changed_after_avalanche_effect = complex_function_encode(open_text, key, ROUNDS, is_key_circular)

    # count difference between changed bits before avalanche and after avalanche effect
    bits_changed_result = []
    for round in range(0, len(bits_changed_after_avalanche_effect)):
        bits_changed_result.append(
            abs(bits_changed_after_avalanche_effect[round] - bits_changed_before_avalanche_effect[round]))
    return bits_changed_result


def plot_avalanche_effect(bit_to_change_index, path_to_binary_key_file, path_to_binary_open_text_file):
    changed_bits_in_rounds = np.append([0], avalanche_effect(bit_to_change_index,
                                                             True,
                                                             path_to_binary_key_file,
                                                             path_to_binary_open_text_file,
                                                             True,
                                                             True))
    plt.plot(np.arange(0, ROUNDS + 1), changed_bits_in_rounds)
    plt.suptitle("Changed bits in key: F=(Vi)=Vi; Circular key;")
    plt.show()

    changed_bits_in_rounds = np.append([0], avalanche_effect(bit_to_change_index,
                                                             True,
                                                             path_to_binary_key_file,
                                                             path_to_binary_open_text_file,
                                                             True,
                                                             False))
    plt.plot(np.arange(0, ROUNDS + 1), changed_bits_in_rounds)
    plt.suptitle("Changed bits in key: F=(Vi)=Vi; Scrambled key;")
    plt.show()

    changed_bits_in_rounds = np.append([0], avalanche_effect(bit_to_change_index,
                                                             True,
                                                             path_to_binary_key_file,
                                                             path_to_binary_open_text_file,
                                                             False,
                                                             True))
    plt.plot(np.arange(0, ROUNDS + 1), changed_bits_in_rounds)
    plt.suptitle("Changed bits in key: F=(Vi,X)=S(X) XOR Vi; Circular key;")
    plt.show()

    changed_bits_in_rounds = np.append([0], avalanche_effect(bit_to_change_index,
                                                             True,
                                                             path_to_binary_key_file,
                                                             path_to_binary_open_text_file,
                                                             False,
                                                             False))
    plt.plot(np.arange(0, ROUNDS + 1), changed_bits_in_rounds)
    plt.suptitle("Changed bits in key: F=(Vi,X)=S(X) XOR Vi; Scrambled key;")
    plt.show()

    changed_bits_in_rounds = np.append([0], avalanche_effect(bit_to_change_index,
                                                             False,
                                                             path_to_binary_key_file,
                                                             path_to_binary_open_text_file,
                                                             True,
                                                             True))
    plt.plot(np.arange(0, ROUNDS + 1), changed_bits_in_rounds)
    plt.suptitle("Changed bits in open text: F=(Vi)=Vi; Circular key;")
    plt.show()

    changed_bits_in_rounds = np.append([0], avalanche_effect(bit_to_change_index,
                                                             False,
                                                             path_to_binary_key_file,
                                                             path_to_binary_open_text_file,
                                                             True,
                                                             False))
    plt.plot(np.arange(0, ROUNDS + 1), changed_bits_in_rounds)
    plt.suptitle("Changed bits in open text: F=(Vi)=Vi; Scrambled key;")
    plt.show()

    changed_bits_in_rounds = np.append([0], avalanche_effect(bit_to_change_index,
                                                             False,
                                                             path_to_binary_key_file,
                                                             path_to_binary_open_text_file,
                                                             False,
                                                             True))
    plt.plot(np.arange(0, ROUNDS + 1), changed_bits_in_rounds)
    plt.suptitle("Changed bits in open text: F=(Vi,X)=S(X) XOR Vi; Circular key;")
    plt.show()

    changed_bits_in_rounds = np.append([0], avalanche_effect(bit_to_change_index,
                                                             False,
                                                             path_to_binary_key_file,
                                                             path_to_binary_open_text_file,
                                                             False,
                                                             False))
    plt.plot(np.arange(0, ROUNDS + 1), changed_bits_in_rounds)
    plt.suptitle("Changed bits in open text: F=(Vi,X)=S(X) XOR Vi; Scrambled key;")
    plt.show()


def main():
    print("------------------------------------------------------------------------------------------------")
    print("--- This program performs encryption and decryption using Feistel cipher algorithm (Bitwise) ---")
    print("------------------------------------------------------------------------------------------------")
    print("Update key and open text in 'data/' directory.")
    print("Choose encryption key mode:\n\t1. Circular encryption of Vi(key)\n\t2. Scrambled encryption of Vi(key)")
    key_mode = input("Encryption key mode: ")

    print("Choose function mode:\n\t1. F=(Vi)=Vi\n\t2. F=(Vi,X)=S(X) XOR Vi")
    fun_mode = input("Function mode: ")

    if fun_mode == "1":
        open_text = check_open_text(open(PATH_TO_OPEN_TEXT_FILE, "r").readline())
        write_binary_open_text_file(PATH_TO_BINARY_OPEN_TEXT_FILE, open_text)

        key = check_key(open(PATH_TO_KEY_FILE, "r").readline(), open_text)
        write_binary_key_file(PATH_TO_BINARY_KEY_FILE, key)

        if key_mode == "1":
            single_function_encode(open_text, key, ROUNDS, True)
            encoded_text = open(PATH_TO_ENCRYPTED_FILE, "r").readline()
            single_function_decode(encoded_text, key, ROUNDS, True)

        elif key_mode == "2":
            single_function_encode(open_text, key, ROUNDS, False)
            encoded_text = open(PATH_TO_ENCRYPTED_FILE, "r").readline()
            single_function_decode(encoded_text, key, ROUNDS, False)

        else:
            raise Exception(KEY_MODE_EXCEPTION)

    elif fun_mode == "2":
        open_text = check_open_text(open(PATH_TO_OPEN_TEXT_FILE, "r").readline())
        write_binary_open_text_file(PATH_TO_BINARY_OPEN_TEXT_FILE, open_text)

        key = check_key(open(PATH_TO_KEY_FILE, "r").readline(), open_text)
        write_binary_key_file(PATH_TO_BINARY_KEY_FILE, key)

        if key_mode == "1":
            complex_function_encode(open_text, key, ROUNDS, True)
            encoded_text = open(PATH_TO_ENCRYPTED_FILE, "r").readline()
            complex_function_decode(encoded_text, key, ROUNDS, True)

        elif key_mode == "2":
            complex_function_encode(open_text, key, ROUNDS, False)
            encoded_text = open(PATH_TO_ENCRYPTED_FILE, "r").readline()
            complex_function_decode(encoded_text, key, ROUNDS, False)

        else:
            raise Exception(KEY_MODE_EXCEPTION)
    else:
        raise Exception(FUNCTION_MODE_EXCEPTION)

    print("Open text: ")
    print(open_text)
    print("Open text (bin): ")
    open_text_bin = open(PATH_TO_BINARY_OPEN_TEXT_FILE, "r").readline()
    print(open_text_bin)
    print("Key: ")
    print(key)
    print("Key (bin):")
    key_bin = open(PATH_TO_BINARY_KEY_FILE, "r").readline()
    print(key_bin)
    print("Encoded text: ")
    print(encoded_text)
    print("Encoded text (bin):")
    encoded_text_bin = open(PATH_TO_BINARY_ENCRYPTED_FILE, "r").readline()
    print(encoded_text_bin)
    print("Decoded text:")
    decoded_text = open(PATH_TO_DECRYPTED_FILE, "r").readline()
    print(decoded_text)
    print("Check results in 'data/' directory")

    plot_avalanche_effect(7, PATH_TO_BINARY_KEY_FILE, PATH_TO_BINARY_OPEN_TEXT_FILE)


if __name__ == '__main__':
    main()
