# Square matrix size
N = 4

grille = [[1, 1, 0, 1],
          [1, 1, 1, 0],
          [1, 0, 1, 1],
          [0, 1, 1, 1]]


# Function to rotate
# N x N matrix by 90 degrees in
# clockwise (dir=1) or in anti-clockwise (n=-1)
# direction
def rotate_matrix(mat, dir):
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
def display_matrix(mat):
    for i in range(0, N):
        for j in range(0, N):
            print(mat[i][j], end='\t')
        print("")

    print()


def main():
    display_matrix(grille)
    rotate_matrix(grille, -1)
    # Print rotated matrix
    display_matrix(grille)


if __name__ == '__main__':
    main()
