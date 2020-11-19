"""
Created on Wed Nov 19 00:44:06 2020
@author: Kyrylo Terentiev
"""


def validate_signed_msg(n, e, signed_msg):
    is_msg_valid = True
    for pair in signed_msg:
        is_pair_valid = validate_pair(n, e, pair)
        print(f'\tn={n}, e={e}, pair={pair}, valid={is_pair_valid}')
        is_msg_valid = is_msg_valid and is_pair_valid

    print(f'message valid={is_msg_valid}')
    return is_msg_valid


def validate_pair(n, e, pair):
    m, s = pair
    return (s ** e) % n == m


def parse_pair(pair):
    pair = pair.replace('(', '').replace(')', '')
    parts = pair.split(',')
    return int(parts[0]), int(parts[1])


def main():
    print("-------------------------------------------------------------------------------")
    print("--- This program performs validation of signed messages using RSA algorithm ---")
    print("-------------------------------------------------------------------------------")
    n = int(input('Enter value of n: '))
    e = int(input('Enter value of e: '))
    message = input('Enter signed message in format (m1,s1) (m2,s2) (m2,s3): ')
    pairs = []
    for p in message.split(' '):
        pairs.append(parse_pair(p))

    validate_signed_msg(n, e, pairs)


if __name__ == '__main__':
    main()
