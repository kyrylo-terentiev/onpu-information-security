"""
Created on Wed Nov 19 02:12:45 2020
@author: Kyrylo Terentiev
"""


p = 23
g = 5


def calculate_y(x):
    return (g ** x) % p


def calculate_b(x, k, m, a):
    b = 0
    while (x * a + k * b) % (p - 1) != m:
        b = b + 1

    return b


def sign_msg(x, k, m):
    a = calculate_y(k)
    b = calculate_b(x, k, m, a)
    return m, a, b


def validate_msg(x, a, b, m):
    y = calculate_y(x)
    print(f'y={y}')
    return ((y ** a) * (a ** b)) % p == (g ** m) % p


def main():
    print("---------------------------------------------------------------------")
    print("--- This program performs message signing using ElGamal algorithm ---")
    print("---------------------------------------------------------------------")
    print(f'p={p}, g={g}')
    x = int(input('Enter value of x (closed key): '))
    k = int(input('Enter value of k: '))
    m = int(input('Enter value of m: '))
    m, a, b = sign_msg(x, k, m)
    print(f'Signed message: m={m}, a={a}, b={b}')
    is_msg_valid = validate_msg(x, a, b, m)
    print(f'valid={is_msg_valid}')


if __name__ == '__main__':
    main()
