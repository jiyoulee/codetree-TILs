from collections import deque

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
de = [
        [(0, -2), (-1, -1), (-2, 0), (-1, 1), (0, 2)],
        [(-2, 0), (-1, 1), (0, 2), (1, 1), (2, 0)],
        [(0, -2), (1, -1), (2, 0), (1, 1), (0, 2)],
        [(-2, 0), (-1, -1), (0, -2), (1, -1), (2, 0)]
     ]

num_rows, num_cols, num_turns = map(int, input().split())
board = [[0] * (num_cols + 2) for _ in range(num_rows + 3)]

def print_global_vars():
    print("board")
    for i in range(num_rows + 3):
        str = ""
        for j in range(num_cols + 2):
            str = " ".join([str, f"{board[i][j]:10}"])
        print(str)
    print("-" * 20)


def get_golem_position(ar: int, ac: int, ad: int):
    global num_rows, num_cols, board

    r, c, d = ar, ac, ad

    while True:
        # 1. move south
        if (
                num_rows + 2 >= (r + 2) and
                1 <= (c - 1) and
                num_cols >= (c + 1) and
                not board[r + 1][c - 1] and
                not board[r + 2][c] and
                not board[r + 1][c + 1]
        ):
                r += 1
        # 2. move west
        elif (
                num_rows + 2 >= (r + 2) and
                1 <= (c - 2) and
                not board[r - 1][c - 1] and
                not board[r][c - 2] and
                not board[r + 1][c - 1] and
                not board[r + 1][c - 2] and
                not board[r + 2][c - 1]
        ):
                r += 1
                c -= 1
                d = (d + 3) % 4
        # 3. move east
        elif (
                num_rows + 2 >= (r + 2) and
                num_cols >= (c + 2) and
                not board[r - 1][c + 1] and
                not board[r][c + 2] and
                not board[r + 1][c + 1] and
                not board[r + 1][c + 2] and
                not board[r + 2][c + 1]
        ):
                r += 1
                c += 1
                d = (d + 1) % 4
        # 4. stop
        else:
            break

    return r, c, d


def set_golem_position(ar: int, ac: int, ad: int, at: int):
    global num_rows, num_cols, board

    flag = True

    r, c, d, t = ar, ac, ad, at

    if 3 <= (r - 1) and num_rows + 2 >= (r + 1) and 1 <= (c - 1) and num_cols >= (c + 1):
        board[r][c] = t

        for dd in range(4):
            cr, cc = r + dr[dd], c + dc[dd]

            if dd == d:
                board[cr][cc] = -t
            else:
                board[cr][cc] = t
    else:
        flag = False

        for i in range(num_rows + 3):
            for j in range(num_cols + 2):
                board[i][j] = 0

    return flag


def get_fairy_position(r: int, c: int):
    global num_rows, num_cols, board

    locr, locc = r, c

    q = deque()
    visited = [[False] * (num_cols + 2) for _ in range(num_rows + 3)]

    q.append((locr, locc))
    visited[locr][locc] = True
    val = locr

    while q:
        curr, curc = q.pop()
        curt = board[curr][curc]

        for di in range(4):
            nextr, nextc = curr + dr[di], curc + dc[di]

            if 3 <= nextr <= (num_rows + 2) and 1 <= nextc <= num_cols and not visited[nextr][nextc]:
                if 0 < curt:
                    if abs(board[nextr][nextc]) == curt:
                        visited[nextr][nextc] = True
                        val = max(val, nextr)
                        q.append((nextr, nextc))
                elif 0 > curt:
                    if board[nextr][nextc]:
                        visited[nextr][nextc] = True
                        val = max(val, nextr)
                        q.append((nextr, nextc))

    return val - 2


answer = 0

for t in range(1, num_turns + 1):
    r = 1
    c, d = map(int, input().split())

    r, c, d = get_golem_position(r, c, d)

    if set_golem_position(r, c, d, t):
        answer += get_fairy_position(r, c)

print(answer)