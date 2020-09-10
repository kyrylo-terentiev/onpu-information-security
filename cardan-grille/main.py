# Square matrix size
N = 4
# default matrix rotation direction (1 - clockwise, -1 - anti-clockwise)
DEFAULT_DIR = 1


# Function to rotate
# N x N matrix by 90 degrees in
# clockwise (dir=1) or in anti-clockwise (n=-1)
# direction
def rotate_matrix(mat, dir):
    if dir != 1 and dir != -1:
        raise ValueError('dir parameter should be 1 (clockwise) or -1 (anti-clockwise)')

    if dir == 1:
        for i in range(0, int(N / 2)):
            for j in range(i, N - i - 1):
                temp = mat[i][j]
                mat[i][j] = mat[N - 1 - j][i]
                mat[N - 1 - j][i] = mat[N - 1 - i][N - 1 - j]
                mat[N - 1 - i][N - 1 - j] = mat[j][N - 1 - i]
                mat[j][N - 1 - i] = temp

    elif dir == -1:
        for i in range(0, int(N / 2)):
            for j in range(i, N - i - 1):
                temp = mat[i][j]
                mat[i][j] = mat[j][N - 1 - i]
                mat[j][N - 1 - i] = mat[N - 1 - i][N - 1 - j]
                mat[N - 1 - i][N - 1 - j] = mat[N - 1 - j][i]
                mat[N - 1 - j][i] = temp


# Function to display matrix
def display_matrix(mat, title):
    print(title)
    for i in range(N):
        for j in range(N):
            print(mat[i][j], end='\t')
        print()

    print()


# Encode input phrase using given cardan grille and it's rotation direction
# into encoded square matrix
def encode(input, grille, dir):
    if dir != 1 and dir != -1:
        raise ValueError('dir parameter should be 1 (clockwise) or -1 (anti-clockwise)')

    if len(input) > pow(N, 2):
        raise ValueError(f'For N={N} input length should not exceed {pow(N, 2)}')

    mat = [['' for i in range(N)] for j in range(N)]
    # current index of input string
    k = 0
    # rotate grille
    for r in range(N):
        # scan current state of grille
        for i in range(N):
            for j in range(N):
                # fill in the encode matrix, if input is not fully encoded yet
                if grille[i][j] == 0 and k < pow(N, 2):
                    mat[i][j] = input[k]
                    k = k + 1
        rotate_matrix(grille, dir)

    return mat


# Decode encoded square matrix using given cardan grille and it's rotation direction
# into initial phrase
def decode(mat, grille, dir):
    if dir != 1 and dir != -1:
        raise ValueError('dir parameter should be 1 (clockwise) or -1 (anti-clockwise)')

    phrase = ['' for i in range(pow(N, 2))]
    k = 0
    for r in range(N):
        for i in range(N):
            for j in range(N):
                if grille[i][j] == 0:
                    phrase[k] = mat[i][j]
                    k = k + 1
        rotate_matrix(grille, dir)

    return ''.join(phrase)


def main():
    # Cardan grille 4*4
    grille = [[1, 1, 0, 1],
              [1, 1, 1, 0],
              [1, 0, 1, 1],
              [0, 1, 1, 1]]

    display_matrix(grille, 'Cardan grille:')
    phrase_to_encode = 'приезжаю шестого'
    print(f'Phrase to encode: {phrase_to_encode}')
    result = encode(phrase_to_encode, grille, DEFAULT_DIR)
    display_matrix(result, 'Encoded matrix:')
    decoded_phrase = decode(result, grille, DEFAULT_DIR)
    print(f'Decoded phrase: {decoded_phrase}')



if __name__ == '__main__':
    main()
