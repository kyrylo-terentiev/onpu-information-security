
def get_russian_abc():
    return ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'ъ', 'э', 'ю', 'я']


def get_english_abc():
    return list(map(chr, range(ord('a'), ord('z') + 1)))


def read_encode_input():
    print('This program performs encoding and decoding of messages using Caesar cipher with a keyword')
    message = input('Enter message to encode: ')
    key = 0
    while not 0 < key < len(get_russian_abc()):
        key = int(input('Enter a desired key (int from 0 to n-1): '))

    keyword = input('Enter a desired keyword: ')
    return message, key, keyword


def read_decode_input():



def validate(message, keyword, abc):
    for i in message:
        if i != ' ' and i not in abc:
            raise ValueError('Message or encoded string should contain only characters of the used alphabet:')
    for i in keyword:
        if i != ' ' and i not in abc:
            raise ValueError('Keyword should contain only characters of the used alphabet:')


def encode(message, key, keyword, abc, debug):
    validate(message, keyword, abc)
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
    validate(encoded, keyword, abc)


def main():
    print('Encoding:')
    message, key, keyword = read_encode_input()
    encoded_message = encode(message, key, keyword, get_english_abc(), 1)
    print(f'Encoded message: {encoded_message}\n')

    print('Decoding:')
    encoded, key, keyword = read_decode_input()
    decoded_message = decode(encoded, key, keyword, get_english_abc(), 1)
    print(f'Decoded message: {decoded_message}\n')


if __name__ == '__main__':
    main()