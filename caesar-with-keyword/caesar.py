def get_english_abc():
    return list(map(chr, range(ord('a'), ord('z') + 1)))


def read_encode_input(abc):
    message = input('Enter message to encode: ')
    key = 0
    while not 0 < key < len(abc):
        key = int(input('Enter a desired key (int from 0 to n-1): '))

    keyword = input('Enter a desired keyword: ')
    return message, key, keyword


def read_decode_input(abc):
    encoded = input('Enter encoded message to decode: ')
    key = 0
    while not 0 < key < len(abc):
        key = int(input('Enter a given key (int from 0 to n-1): '))

    keyword = input('Enter a given keyword: ')
    return encoded, key, keyword


def validate(message, keyword, abc):
    for i in message:
        if i != ' ' and i not in abc:
            raise ValueError('Message or encoded string should contain only characters of the used alphabet:')
    for i in keyword:
        if i != ' ' and i not in abc:
            raise ValueError('Keyword should contain only characters of the used alphabet:')


def encode(message, key, keyword, abc, debug):
    # save spaces indices
    spaces_ind = []
    for i in range(0, len(message)):
        if message[i] == ' ':
            spaces_ind.append(i)

    # remove spaces
    msg = message.replace(' ', '')
    # initialize new alphabet
    new_abc = ['' for i in range(len(abc))]

    # alphabet without letters from keyword
    rest_abs = abc.copy()
    for i in rest_abs:
        if i in keyword:
            rest_abs.remove(i)

    # place keyword into new alphabet
    j = key
    for i in keyword:
        new_abc[j] = i
        j = j + 1

    # fill new alphabe with rest of letters
    j = 0
    for i in range(key + len(keyword), len(new_abc)):
        new_abc[i] = rest_abs[j]
        j += 1

    for i in range(0, key):
        new_abc[i] = rest_abs[j]
        j += 1

    # encode message
    encoded = ''
    j = 0
    for i in msg:
        if j in spaces_ind:
            encoded = encoded + ' '
        index = abc.index(i)
        encoded = encoded + new_abc[index]
        j = j + 1

    if debug == 1:
        print('DEBUG MODE ON')
        print('-------------------------------------------------------------')
        print(f'Message: {message}\nKey: {key}\nKeyword: {keyword}')
        print(f'Old alphabet:  \t{abc}')
        print(f'New alphabet:  \t{new_abc}')
        print(f'Input msg:  \t{message}')
        print(f'Encoded msg: \t{encoded}')
        print('-------------------------------------------------------------')

    return encoded


def decode(encoded, key, keyword, abc, debug):
    # save spaces indices
    spaces_ind = []
    for i in range(0, len(encoded)):
        if encoded[i] == ' ':
            spaces_ind.append(i)

    # remove spaces
    msg = encoded.replace(' ', '')
    # initialize new alphabet
    new_abc = ['' for i in range(len(abc))]

    # alphabet without letters from keyword
    rest_abs = abc.copy()
    for i in rest_abs:
        if i in keyword:
            rest_abs.remove(i)

    # place keyword into new alphabet
    j = key
    for i in keyword:
        new_abc[j] = i
        j = j + 1

    # fill new alphabe with rest of letters
    j = 0
    for i in range(key + len(keyword), len(new_abc)):
        new_abc[i] = rest_abs[j]
        j += 1

    for i in range(0, key):
        new_abc[i] = rest_abs[j]
        j += 1

    # decode message
    decoded = ''
    j = 0
    for i in msg:
        if j in spaces_ind:
            decoded = decoded + ' '
        index = new_abc.index(i)
        decoded = decoded + abc[index]
        j = j + 1

    if debug == 1:
        print('ENCODE MODE ON')
        print('-------------------------------------------------------------')
        print(f'Encoded: {encoded}\nKey: {key}\nKeyword: {keyword}')
        print(f'Old alphabet:  \t{abc}')
        print(f'New alphabet:  \t{new_abc}')
        print(f'Input msg:  \t{encoded}')
        print(f'Decoded msg: \t{decoded}')
        print('-------------------------------------------------------------')

    return decoded


def main():
    print('This program performs encoding and decoding of messages using Caesar cipher with a keyword')
    print('Encoding:')
    abc = get_english_abc()
    message, key, keyword = read_encode_input(abc)
    validate(message, keyword, abc)
    encoded_message = encode(message, key, keyword, abc, 1)
    print(f'Encoded message: {encoded_message}\n')

    print('Decoding:')
    encoded, key, keyword = read_decode_input(abc)
    validate(encoded, keyword, abc)
    decoded_message = decode(encoded, key, keyword, get_english_abc(), 1)
    print(f'Decoded message: {decoded_message}\n')


if __name__ == '__main__':
    main()