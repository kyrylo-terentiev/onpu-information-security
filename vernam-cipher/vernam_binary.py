import binascii

def encrypt(key, message):
    print(f'Incoming message >>> \t\t{message}')
    print(f'Key >>> \t\t\t\t\t{key}')
    print(f'Incoming message (bin) >>> \t{bin(int(binascii.hexlify(message.encode()), 16))}')
    print(f'Key (bin) >>> \t\t\t\t{bin(int(binascii.hexlify(key.encode()), 16))}')

    encrypted_message = ""
    index = 0
    for char in message:
        encrypted_message = encrypted_message + chr(ord(char) ^ ord(key[index]))
        index = index + 1
        if index == len(key):
            index = 0

    return bin(int(binascii.hexlify(encrypted_message.encode()), 16))


def decrypt(key, message):
    message = binascii.unhexlify("%x" % int(message, 2))

    decrypted_message = ""
    index = 0
    for char in message:
        decrypted_message = decrypted_message + chr(char ^ ord(key[index]))
        index = index + 1
        if index == len(key):
            index = 0

    print(f'Decrypted message (bin) >>> ' + bin(int(binascii.hexlify(decrypted_message.encode()), 16)))

    return decrypted_message


def main():
    message = 'secret';
    key = 'key'
    encrypted_message = encrypt(key, message)
    print(f'Encrypted message >>> \t\t{encrypted_message}')
    decrypted_message = decrypt(key, encrypted_message)
    print(f'Decrypted message >>> \t\t{decrypted_message}')


if __name__ == "__main__":
    main()
