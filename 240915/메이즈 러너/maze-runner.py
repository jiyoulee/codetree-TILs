N, M, K = map(int, input().split())

board = [[0] * (N + 1) for _ in range(N + 1)]
for r in range(1, N + 1):
    row = list(map(int, input().split()))
    for c in range(1, N + 1):
        board[r][c] = row[c - 1]

persons = [(0, 0)] + [tuple(map(int, input().split())) for _ in range(M)]
status = [1] * (M + 1)
status[0] = 0
d4 = [(0, -1), (0, 1), (-1, 0), (1, 0)]

door = tuple(map(int, input().split()))

def in_range(r: int, c: int):
    global N
    return 1 <= r <= N and 1 <= c <= N


def get_loc(person: tuple[int, int]):
    loc = (0, 0)

    r, c = person
    l = abs(door[0] - r) + abs(door[1] - c)

    for d in range(4):
        nr, nc = r + d4[d][0], c + d4[d][1]
        nl = abs(door[0] - nr) + abs(door[1] - nc)

        if in_range(nr, nc) and board[nr][nc] <= 0 and nl < l:
            loc = (nr, nc)

    return loc


def get_square_loc():
    cases = []
    for i in range(1, M + 1):
        if status[i]:
            cases.append((persons[i][0], persons[i][1], max(abs(door[0] - persons[i][0]), abs(door[1] - persons[i][1]))))
    cases.sort(key=lambda x: (x[2], x[0], x[1]))

    r, c, l = cases[0]
    rdif = abs(door[0] - r)
    cdif = abs(door[1] - c)

    if rdif >= cdif:
        loc = (min(r, door[0]), max(1, max(c, door[1]) - rdif))
    else:
        loc = (max(1, max(r, door[0]) - cdif), min(c, door[1]))

    return loc, l


def rotate_board(loc, l: int):
    global board

    r, c = loc
    boardC = [[0] * (N + 1) for _ in range(N + 1)]

    for i in range(r, r + l + 1):
        for j in range(c, c + l + 1):
            boardC[i][j] = board[i][j]

    for i in range(0, l + 1):
        for j in range(0, l + 1):
            board[i + r][j + c] = boardC[-j + r + l][i + c] - 1


def rotate_persons(loc, l):
    global persons

    r, c = loc

    for i in range(1, M + 1):
        if status[i] and r <= persons[i][0] <= r + l and c <= persons[i][1] <= c + l:
            difr = persons[i][0] - r
            difc = persons[i][1] - c
            persons[i] = (difc + r, -difr + c + l)


def rotate_door(loc, l):
    global door

    r, c = loc
    difr = door[0] - r
    difc = door[1] - c
    door = (difc + r, -difr + c + l)



def main():
    global persons, board

    answer = 0

    for k in range(1, K + 1):
        for m in range(1, M + 1):
            if status[m]:
                loc = get_loc(persons[m])

                if not loc[0]:
                    continue

                answer += 1
                persons[m] = loc

                if loc != door:
                    continue

                status[m] = 0

        if not sum(status):
            break

        loc, l = get_square_loc()

        rotate_board(loc, l)
        rotate_persons(loc, l)
        rotate_door(loc, l)

    print(answer)
    print(door[0], door[1])

if __name__ == "__main__":
    main()